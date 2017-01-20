#!/usr/bin/env python
import argparse
import getpass
import json
import logging

import neutronclient
import os

import os_client_config
from keystoneclient.v2_0.client import Client as Keystone
from novaclient.client import Client as Nova
from neutronclient.v2_0.client import Client as Neutron
from keystoneauth1.session import Session
from openstack import connection
from openstack.identity.v3.user import User
from openstack.identity.v3.project import Project
from openstack.compute.v2.server import ServerDetail
from openstack.compute.v2.keypair import Keypair
from openstack.network.v2.network import Network
from openstack.network.v2.subnet import Subnet

logger = logging.getLogger("org.openbaton.openstack.SetUpper")
NETWORKS = ["mgmt", "net_a", "net_b", "net_c", "net_d", "private"]
# NETWORKS = ["test"]
ob_project = None


def get_user_by_username(username, keystone):
    users = keystone.users.list()
    for user in users:
        if user.name == username:
            return user


def get_role(role_to_find, keystone):
    roles = keystone.roles.list()
    for role in roles:
        if role.name == role_to_find:
            return role


def create_project(keystone, tenant_name, username):
    ob_tenant = None
    user = get_user_by_username(username, keystone)
    role = get_role('admin', keystone)
    for tenant in keystone.tenants.list():
        if tenant.name == tenant_name:
            logger.warn("Tenant with name or id %s exists already! i am going to mess it up :)" % tenant_name)
            ob_tenant = tenant
            if len([role_ for role_ in keystone.users.list_roles(user=user, tenant=ob_tenant) if
                    role_.name == 'admin']) > 0:
                logger.warn("User %s has already admin role in %s tenant" % (username, tenant_name))
                return ob_tenant
            break
    if ob_tenant is None:
        ob_tenant = keystone.tenants.create(tenant_name=tenant_name, description='openbaton tenant')
        logger.debug("Created tenant with id: %s" % ob_tenant.id)

    keystone.roles.add_user_role(user=user, role=role, tenant=ob_tenant)
    return ob_tenant


def get_ext_net(neutron):
    return [ext_net for ext_net in neutron.list_networks()['networks'] if ext_net['router:external']][0]


def create_keypair(nova):
    for keypair in nova.keypairs.list():
        if keypair.name == "openbaton":
            return keypair
    kargs = {"name": "openbaton"}
    keypair = nova.keypairs.create(**kargs)
    with open("./openbaton.pem", "w") as f:
        try:
            f.write(keypair.private_key)
        except TypeError:
            logger.warn("I hope you did not loose the private key of the openbaton keypair...")
    return keypair


def create_networks_and_subnets(neutron, ext_net, router_name='ob_router'):
    networks = []
    subnets = []
    ports = []
    router_id = None
    exist_net = [network for network in neutron.list_networks()['networks']]
    exist_net_names = [network['name'] for network in exist_net]
    net_name_to_create = [net for net in NETWORKS if net not in exist_net_names]
    networks.extend(network for network in exist_net if network['name'] in NETWORKS)
    index = 1
    for net in net_name_to_create:
        kwargs = {'network': {
            'name': net,
            'shared': False,
            'admin_state_up': True
        }}
        logger.debug("Creating net %s" % net)
        network_ = neutron.create_network(body=kwargs)['network']
        networks.append(network_)
        kwargs = {
            'subnets': [
                {
                    'name': "subnet_%s" % net,
                    'cidr': "192.168.%s.0/24" % index,
                    'gateway_ip': '192.168.%s.1' % index,
                    'ip_version': '4',
                    'enable_dhcp': True,
                    'dns_nameservers': ['8.8.8.8'],
                    'network_id': network_['id']
                }
            ]
        }
        logger.debug("Creating subnet subnet_%s" % net)
        subnet = neutron.create_subnet(body=kwargs)
        subnets.append(subnet)

        router = get_router_from_name(neutron, router_name, ext_net)
        router_id = router['router']['id']

        body_value = {
            'subnet_id': subnet['subnets'][0]['id'],
        }
        try:
            ports.append(neutron.add_interface_router(router=router_id, body=body_value))
        except Exception as e:
            pass
        index += 1

    return networks, subnets, router_id


def get_router_from_name(neutron, router_name, ext_net):
    for router in neutron.list_routers()['routers']:
        if router['name'] == router_name:
            return neutron.show_router(router['id'])
    request = {'router': {'name': router_name, 'admin_state_up': True}}
    router = neutron.create_router(request)
    body_value = {"network_id": ext_net['id']}
    neutron.add_gateway_router(router=router['router']['id'], body=body_value)
    return router


def associate_router_to_subnets(networks, neutron, router_name='ob_router'):
    router = get_router_from_name(neutron, router_name, ext_net)
    router_id = router['router']['id']

    ports = []
    for network in networks:
        logger.dubug("checking net: %s" % network['name'])
        net_has_int = False
        for port in neutron.list_ports()['ports']:
            logger.dubug("Checking port:\n%s" % port)
            if port['network_id'] == network['id']:
                body_value = {
                    'subnet_id': network['subnets'][0],
                }
                try:
                    ports.append(neutron.add_interface_router(router=router_id, body=body_value))
                except Exception as e:
                    print e.message
                net_has_int = True
        if not net_has_int:
            body_value = {'port': {
                'admin_state_up': True,
                'device_id': router_id,
                'name': 'ob_port',
                'network_id': network['id'],

                # 'network_id': subnet['id'],
            }}
            logger.dubug("Creating port: %s" % body_value['port']['name'])
            ports.append(neutron.create_port(body=body_value))

    return router, ports


def allocate_floating_ips(neutron, fip_num):
    body = {"floatingip": {"floating_network_id": ext_net['id']}}
    for i in range(fip_num):
        try:
            neutron.create_floatingip(body=body)
        except neutronclient.common.exceptions.IpAddressGenerationFailureClient as e:
            logger.error("Not able to allocate floatingips :(")
            return


def create_rule(neutron, sec_group, protocol):
    body = {"security_group_rule": {
        "direction": "ingress",
        "port_range_min": "1",
        "port_range_max": "65535",
        # "name": sec_group['security_group']['name'],
        "security_group_id": sec_group['security_group']['id'],
        "remote_ip_prefix": "0.0.0.0/0",
        "protocol": protocol,
    }}
    if protocol == 'icmp':
        body['security_group_rule'].pop('port_range_min', None)
        body['security_group_rule'].pop('port_range_max', None)
    try:
        neutron.create_security_group_rule(body=body)
    except neutronclient.common.exceptions.Conflict as e:
        pass



def create_security_group(neutron, sec_group_name='ob_sec_group'):
    sec_group = {}
    for sg in neutron.list_security_groups()['security_groups']:
        if sg['name'] == sec_group_name:
            sec_group['security_group'] = sg
            break
    if len(sec_group) == 0:
        body = {"security_group": {
            'name': sec_group_name,
            'description': 'openbaton security group',
        }}
        sec_group = neutron.create_security_group(body=body)
    create_rule(neutron, sec_group, 'tcp')
    create_rule(neutron, sec_group, 'udp')
    create_rule(neutron, sec_group, 'icmp')
    return sec_group['security_group']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant-name",
                        help="the tenant name to creaton in openstack, default 'openbaton'")
    parser.add_argument("-u", "--username", help="the openstack username")
    parser.add_argument("-p", "--password", help="the openstack password")
    parser.add_argument("-d", "--debug", help="show debug prints", action="store_true")
    parser.add_argument("-f", "--fip-num", help="number of floating ip to allocate", default=7, type=int)
    parser.add_argument("--auth-url", help="the openstack auth url")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    username = os.environ.get('OS_USERNAME')
    password = os.environ.get('OS_PASSWORD')
    auth_url = os.environ.get("OS_AUTH_URL")
    tenant_name_for_auth = os.environ.get("OS_TENANT_NAME")
    tenant_name = None
    # tenant_name = os.environ.get("OS_TENANT_ID")

    fip_num = args.fip_num

    if args.username is not None:
        username = args.username
    if args.password is not None:
        password = args.password
    if args.auth_url is not None:
        auth_url = args.auth_url
    if args.tenant_name is not None:
        tenant_name = args.tenant_name

    if username is None or username == "":
        username = raw_input("insert user: ")
    if auth_url is None or auth_url == "":
        auth_url = raw_input("insert auth_url: ")
    if password is None or password == "":
        password = getpass.getpass("insert password: ")

    if tenant_name is None:
        tenant_name = 'openbaton'

    logger.debug("username: '%s'" % username)
    logger.debug("password: '%s'" % password)
    logger.debug("tenant_name: '%s'" % tenant_name_for_auth)
    logger.debug("auth_url: '%s'" % auth_url)

    keystone = Keystone(username=username, password=password, auth_url=auth_url, tenant_name=tenant_name_for_auth)
    ob_project = create_project(keystone=keystone, tenant_name=tenant_name, username=username)

    neutron = Neutron(username=username,
                      password=password,
                      project_name=tenant_name,
                      auth_url=auth_url)

    ext_net = get_ext_net(neutron)
    if ext_net is None:
        logger.error("A shared  External Network must exist! Please create one in your openstack instance")
        exit(2)

    credentials = {
        # 'version': '2',
        # 'username': username,
        # 'api_key': password,
        'password': password,
        # 'auth_url': auth_url,
        'project_name': tenant_name_for_auth,
        'tenant_name': tenant_name
    }
    nova = Nova('2', username, password, ob_project.name, auth_url)
    keypair = create_keypair(nova)

    router_id = None
    networks, subnets, _ = create_networks_and_subnets(neutron, ext_net)

    allocate_floating_ips(neutron, fip_num=fip_num)

    sec_group = create_security_group(neutron)

    vim_instance = {
        "name": "vim-instance",
        "authUrl": auth_url,
        "tenant": tenant_name,
        "username": username,
        "password": password,
        "keyPair": keypair.name,
        "securityGroups": [
            sec_group['name']
        ],
        "type": "openstack",
        "location": {
            "name": "Berlin",
            "latitude": "52.525876",
            "longitude": "13.314400"
        }
    }
    with open("vim-instance.json", "w") as f:
        f.write(json.dumps(vim_instance))
