  <img src="https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/openBaton.png" width="250"/>
  
  Copyright © 2015-2016 [Open Baton](http://openbaton.org). 
  Licensed under [Apache v2 License](http://www.apache.org/licenses/LICENSE-2.0).

# Open Baton Bootstrap

This repository contains a number of deployment templates and instructions how to install Open Baton in containers.

The [Quick Start](#quick-start) provides the easiest and fastest way to bring up a working Open Baton framework without caring about any configuration. In addition, there are some other templates provided for different scenarios (check [Available Scenarios](#available-scenarios)) allowing a better way of configuration and versioning

How versioning is managed, you can check [here](#versioning).

## System Requirements
You will need:
- [Docker](https://www.docker.com/community-edition#/download) (>=18.03)
- [Docker Compose](https://docs.docker.com/compose/install/) (>=1.20)
- A checkout of this repository

## Quick Start
In one command you can start Open Baton by using docker-compose and the docker-compose.yml in this repository. 

It downloads the docker-compose.yml in the current folder via `curl` and executes `docker-compose up`. All configurations are contained in this compose file. Only the **HOST_IP** must be set to the actual IP of your host machine so that the virtual machines' Generic EMS can connect to the Generic VNFM via RabbitMQ. Below the command to use:

```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/openbaton/bootstrap/master/docker-compose.yml | env HOST_IP=$YOUR_LOCAL_IP docker-compose up -d
``` 

This basic deployment setup is there for a quick start and contains the following components:
* NFVO
* Generic VNFM
* Openstack4j driver
* Docker VNFM
* Docker driver
* RabbitMQ
* MySQL

These components are enough to make deployments in OpenStack and Docker.

Alternatively, you can also clone this repository via *git* and making use directly the docker-compose.yml by issuing [up](https://docs.docker.com/compose/reference/up/) command. It is important that you set the handed over env variable **HOST_IP** to the reachable IP of your workstation so that deployed VM's can reach the generic VNFM.

```bash
$ env HOST_IP=$YOUR_LOCAL_IP docker-compose up -d
```

You can use a simple curl loop to check if the orchestrator is up and running:
```bash
$ until curl -sSf --stderr /dev/null http://localhost:8080; do printf '.' && sleep 5;done
```

Alternatively, you can also check the logs of the orchestrator: 

```bash
$ docker-compose logs -f nfvo
```

Once Open Baton has started, you can reach the NFVO's dashboard with your webbrowser at http://localhost:8080

## Versioning
Versioning is provided via GitHub branches and tags within this repository.

* **master** contains always the latest version of all components. Those images are automatically generated and pushed to Docker Hub every time a new commit is done. 
* **tags** the name of the tag indicates the corresponding release version of Open Baton. A list of available versions can be found [here][bootstrap-tags].

**Note**: A change between versions, so branches and tags, can be done with the following comment:

```bash
$ git checkout <branch/tag>
```

## Available components
Most of the Open Baton components are available as Docker images and can easily be started, either via docker-compose making use of deployment templates (check [Available Scenarios](#available-scenarios)) or separately via docker directly (check [Plug-and-Play](#plug-and-play)). A set of utils are provided as well which are used by OpenBaton for communication, persistency or monitoring.

Open Baton components in a nutshell:
* [NFVO][github-nfvo]: NFV Orchestrator, main component of Open Baton (requires RabbitMQ as the central communication system)
* [Generic VNFM][github-vnfm-generic]: enabling generic lifecycle management of VNFs in combination with the Generic EMS
* [OpenStack4j driver][github-driver-openstack4j]: used to manage virtual resources via OpenStack 
* [Docker VNFM][github-vnfm-docker]: enabling container deployments via Docker (works together with the Docker driver) 
* [Docker driver][github-driver-docker] used to manage virtual resources via Docker
* [Dummy VNFM][github-vnfm-dummy]: enabling simple deployments without any lifecycle management 
* [Test driver] [github-driver-test]: used to fake deployments of virtual resources so can be used for testing NFVO and VNF Manager workflows
* [Autoscaling Engine][github-ase]: provides autoscaling capabilities as an external component (requires monitoring system and plugin) 
* [Network Slicing Engine][github-nse]: provides network slicing cababiltites as an external component
* [Zabbix plugin][github-zabbix-plugin]: monitoring plugin to retrieve measurements from Zabbix monitoring system 

Utils:
* [RabbitMQ][web-rabbitmq]: is the central communication system where all components are connected to
* [MySQL][web-mysql]: standard database solution to provide persistency 
* [Zabbix][web-zabbix]: Monitoring system that is intergrated with the Generic VNFM

## Available scenarios 
Below you can find a number of different scenarios. **default** is the scenario used also in the [Quick Start](#quick-start) that is self-container and doesn't make use of any external configuration and/or environment files. The rest of the scenarios make use of external files such as versioning or passing environment files for better configuration (check [here](#configuration-files)). Moreover, dependencies between services themself are always defined in the docker-compose file itself.

The name of the scenario indicates the main functionality provided and identifies also the docker-compose file that provides all services required for that.

Basic usage:
```bash
$ docker-compose -f <DOCKER_COMPOSE_FILE> up -d
```

**Note** This provides also some examples how to configure different environments. Adding or removing services can easily be achives (e.g. using an external MySQL or RabbitMQ installation). Moreover, any setup can be extended by plugging-in other components (check [Plug-and-Play](#plug-and-play)).

**Note** '**NFVO_IP**' should always be set/provided. Especially the Generic VNFM won't work without it.

### **default** ([``docker-compose.yml``](docker-compose.yml)):
Provides a self-contained template providing an Open Baton setup to make deployments in OpenStack and Docker. Check [Quick Start](#quick-start) to see purpose and basic usage.

Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Generic VNFM
* OpenStack4j driver
* Docker VNFM
* Docker driver

### **Minimal setup** ([``docker-compose-minimal.yml``](docker-compose-minimal.yml))
Provides a minimal setup containing the NFVO, communication sytem and persistency.

Contains the following components:
* NFVO
* RabbitMQ
* MySQL

### **OpenStack Deployments** ([``docker-compose-openstack.yml``](docker-compose-openstack.yml))
Provides a setup that allows deployments and lifecycle management of VNFs by allocating virtual resources (e.g. Virtual Machines) in OpenStack. 

Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Generic VNFM
* OpenStack4j driver

### **Docker Deployments** ([``docker-compose-docker.yml``](docker-compose-docker.yml))
Provides a setup that allows deployments of VNFs by allocating virtual resources (e.g. Containers) in via Docker.

Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Docker VNFM
* Docker driver

### **Dummy Deployments** ([``docker-compose-dummy.yml``](docker-compose-dummy.yml))
Provides a setup that allows deployments of VNFs without allocating virtual resources. Can be used for testing.

Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Dummy VNFM
* Test driver

### **Auto Scaling** ([``docker-compose-ase.yml``](docker-compose-ase.yml))
Provides a setup that allows deployments and lifecycle management of VNFs by allocating virtual resources (e.g. Virtual Machines) in OpenStack. In addition, it provides also autoscaling capabilties by making use of Zabbix as the monitoring system. 

Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Generic VNFM
* OpenStack4j driver
* Zabbix monitoring plugin
* Zabbix (required additional configuration via the Zabbix dashboard, check [here][zabbix-config])
* Autoscaling engine

### **Network Slicing** ([``docker-compose-nse.yml``](docker-compose-nse.yml))
Provides a setup that allows deployments and lifecycle management of VNFs by allocating virtual resources (e.g. Virtual Machines) in OpenStack. In addition, it provides network slicing capabilites.  


Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Generic VNFM
* OpenStack4j driver
* Network Slicing Engine

### **full** ([``docker-compose-full.yml``](docker-compose-full.yml))
Provides a setup that contains all the components of all the scenarios above.  

Contains the following components:
* NFVO
* RabbitMQ
* MySQL
* Generic VNFM
* OpenStack4j driver
* Docker VNFM
* Docker driver
* Dummy VNFM
* Test driver
* Zabbix monitoring plugin
* Zabbix (requires additional configuration via the Zabbix dashboard, check [here][zabbix-config])
* Autoscaling engine
* Network Slicing Engine

## Configuration files ##
The following configuration files are used by the corresponding scenarios if those components are used. 

**Note** The `default` scenario doesn't use any external configuration/environment file (everything is contained in the docker-compose file itself in this case).

### Versioning - [./.env](.env)
The file [./.env](.env) contains the versioning for all components. Versions are preset within this file and managed via branches and tags. Nevertheless, you may change manually to set the version of the Docker images to use.

The Open Baton components are set always to `latest` in the *master* branch and to the corresponding release version in the [tags][bootstrap-tags].
The RabbitMQ and MySQL version is set to the compliant version tested together with Open Baton.

```bash
# Open Baton version for (all) components
OB_VERSION=...

OB_ASE_VERSION=...

OB_NSE_VERSION=...

# MySQL used by NFVO
OB_MYSQL_VERSION=...

# RabbitMQ used by Open Baton
OB_RABBITMQ_VERSION=...
```

### Open Baton configuration - [./env/openbaton.env](env/openbaton.env)
The file [./env/openbaton.env](env/openbaton.env) contains all configuration parameters related to Open Baton. Those parameters are passed as environment variables to the containers when launching them.

Besides the basic variables provided via the this configuration file you can also check the corresponding configuration guides of the relevant component and provide other configuration   

**Note** The only variable that must be changed here is the `NFVO_HOST` to the IP of your host machine that is reachable by the VMs. Alternatively, you can also set it via the command line when deploying:  

```bash
$ env HOST_IP=$YOUR_LOCAL_IP docker-compose -f docker-compose-minimal.yml up -d
```

### Zabbix configuration - [./env/zabbix.env](env/zabbix.env)



## Plug-and-play

This section provides a couple of Docker commands to start containers separately. Step-by-step you can start new components and play around:

Requirements:
* RabbitMQ
* MySQL

Those two services can simply be started by using the docker-compose files located in `utils/`. Change to the respective folder and issue a: 

```bash
docker-compose up
```

**Note** RabbitMQ is the central message bus and all components need to connect to it. Therefore, the `RABBITMQ_HOST` parameter that is passed for every container must be reachable from inside the container. Typically, this is the IP of your host machine.      
 
### NFVO
```bash
docker run -p 8080:8080 -e NFVO_RABBIT_BROKERIP=${RABBITMQ_HOST} openbaton/nfvo:latest
```

Parameters:
* `NFVO_RABBIT_BROKERIP` is the reachable IP of the NFVO and RabbitMQ server expecting that both is running on the same host. If this is not the case, you can specify `SPRING_RABBITMQ_HOST` to set the RabbitMQ endpoint separately. 
* (Optional) `MONITORING_IP` can be optionally defined if a default monitoring system is used. Otherwise, the monitoring IP must be defined while launching a new network service. 
* (Optional) `SPRING_PROFILES_ACTIVE` By `default` it is an in memory database. To achieve persistency, the datasource profile must be changed `mysql`
* (Optional) `SPRING_DATASOURCE_URL` Additionally, the MySQL endpoint must be provided in the following way: `jdbc:mysql://<MYSQL_HOST>:3306/openbaton?useSSL=false`. By default it is using the following credentials: `SPRING_DATASOURCE_USERNAME=admin` and `SPRING_DATASOURCE_PASSWORD=changeme`.


### Generic VNFM
```bash
$ docker run -e VNFM_RABBITMQ_BROKERIP=<RABBITMQ_HOST> openbaton/vnfm-generic:latest
```

### Openstack4j driver
```bash
$ docker run -e RABBITMQ=${RABBITMQ_HOST} openbaton/plugin-vimdriver-openstack-4j:latest
```

### Openstack python driver
```bash
$ docker run -e RABBITMQ_IP=${RABBITMQ_HOST} openbaton/plugin-vimdriver-openstack-python:latest
```

### Docker VNFM
```bash

```

### Docker driver
```bash
$ docker run -e BROKER_IP=${RABBITMQ_HOST} -v /var/run/docker.sock:/var/run/docker.sock:rw openbaton/driver-docker-go:latest
```

### Zabbix Monitoring plugin
```bash
$ docker run -p10051:10051 -e ZABBIX_PLUGIN_IP=<ZABBIX_PLUGGIN_IP> -e ZABBIX_HOST=<ZABBIX_HOST> -e RABBITMQ_BROKERIP=${RABBITMQ_HOST} -e ZABBIX_ENDPOINT=/api_jsonrpc.php -e ZABBIX_PORT=80 openbaton/zabbix-plugin:latest
```

Parameters:
* `RABBITMQ_BROKERIP` is the IP where RabbitMQ is reachable
* `ZABBIX_PLUGIN_IP` is the reachable IP where the Zabbix plugin is running 
* `ZABBIX_HOST` is the IP where the Zabbix monitoring is reachable

**Note** A docker-compose template for a containerized Zabbix is also available in `utils/`.

### Autoscaling Engine
```bash
$ docker run -p 9999:9999 -e ASE_SERVER_IP=<ASE_SERVER_IP> -e NFVO_IP=<NFVO_IP> -e ASE_RABBITMQ_BROKERIP=${RABBITMQ_HOST} openbaton/ase:latest
```

Parameters:
* `ASE_RABBITMQ_BROKERIP` is the IP where RabbitMQ is reachable
* `ASE_SERVER_IP` is the IP where the ASE is reachable 
* `NFVO_IP` is the IP where the NFVO is reachable

 **Note** The Autoscaling Engine requries the Zabbix plugin and a configured Zabbix monitoring system running. 
   
### Network Slicing Engine

```bash
$ docker run -e NFVO_IP=<NFVO_IP> -e RABBITMQ_HOST=${RABBITMQ_HOST} openbaton/nse:latest
```

* `RABBITMQ_HOST` is the IP where RabbitMQ is reachable
* `NFVO_IP` is the IP where the NFVO is reachable 

## Related commands
This section provides some useful commands. 

Important to note here is that the docker-compose file must be provided in every request, except the name of the target file is `docker-compose.yaml` or `docker-compose.yml`. 


To list all running containers execute:
```bash
$ docker-compose -f docker-compose-openstack.yml ps
                 Name                               Command                       State                           Ports
---------------------------------------------------------------------------------------------------------------------------------------
bootstrap_nfvo_1                         java -jar /nfvo.jar              Up                      0.0.0.0:8080->8080/tcp
bootstrap_nfvo_database_1                /entrypoint.sh mysqld            Up (health: starting)   3306/tcp, 33060/tcp
bootstrap_plugin_vimdriver_openstack_4   sh -c java -jar /plugin-vi ...   Restarting
j_1
bootstrap_rabbitmq_broker_1              docker-entrypoint.sh rabbi ...   Up                      15671/tcp, 0.0.0.0:15672->15672/tcp,
                                                                                                  25672/tcp, 4369/tcp, 5671/tcp,
                                                                                                  0.0.0.0:5672->5672/tcp
bootstrap_vnfm_generic_1                 java -jar /vnfm-generic.jar      Up
```

To attach to one of the running containers (e.g. NFVO) with an interactive shell:
```bash
$ docker exec -ti bootstrap_nfvo_1 sh
/ #
```

To attach to the logs of all the running services (drop the -f to only dump "what-is"):
```bash
$ docker-compose -f docker-compose-openstack.yml logs -f
[...]
```

**Note** You may also provide the service names to filter the logs.

To dispose a deployment:
```bash
$ $ docker-compose -f docker-compose-openstack.yml down
Stopping bootstrap_plugin_vimdriver_openstack_4j_1 ... done
Stopping bootstrap_vnfm_generic_1                  ... done
Stopping bootstrap_nfvo_1                          ... done
Stopping bootstrap_nfvo_database_1                 ... done
Stopping bootstrap_rabbitmq_broker_1               ... done
Removing bootstrap_plugin_vimdriver_openstack_4j_1 ... done
Removing bootstrap_vnfm_generic_1                  ... done
Removing bootstrap_nfvo_1                          ... done
Removing bootstrap_nfvo_database_1                 ... done
Removing bootstrap_rabbitmq_broker_1               ... done
Removing network bootstrap_default
```

To restart only a single service, e.g. after changing ENV variables of the openstackplugin in the compose file:
```bash
$ docker-compose -f docker-compose-openstack.yml up -d --no-deps nfvo
Recreating bootstrap_nfvo_1
```

## Issue tracker

Issues and bug reports should be posted to the GitHub Issue Tracker of this project

# What is Open Baton?

OpenBaton is an open source project providing a comprehensive implementation of the ETSI Management and Orchestration (MANO) specification.

Open Baton is a ETSI NFV MANO compliant framework. Open Baton was part of the OpenSDNCore (www.opensdncore.org) project started almost three years ago by Fraunhofer FOKUS with the objective of providing a compliant implementation of the ETSI NFV specification. 

Open Baton is easily extensible. It integrates with OpenStack, and provides a plugin mechanism for supporting additional VIM types. It supports Network Service management either using a generic VNFM or interoperating with VNF-specific VNFM. It uses different mechanisms (REST or PUB/SUB) for interoperating with the VNFMs. It integrates with additional components for the runtime management of a Network Service. For instance, it provides autoscaling and fault management based on monitoring information coming from the the monitoring system available at the NFVI level.

## Source Code and documentation

The Source Code of the other Open Baton projects can be found [here][openbaton-github] and the documentation can be found [here][openbaton-doc] .

## News and Website

Check the [Open Baton Website][openbaton]
Follow us on Twitter @[openbaton][openbaton-twitter].

## Licensing and distribution
Copyright [2015-2016] Open Baton project

Licensed under the Apache License, Version 2.0 (the "License");

you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Support
The Open Baton project provides community support through the Open Baton Public Mailing List and through StackOverflow using the tags openbaton.

## Supported by
  <img src="https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/fokus.png" width="250"/><img src="https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/tu.png" width="150"/>

[fokus-logo]: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/fokus.png
[openbaton]: http://openbaton.org
[openbaton-doc]: http://openbaton.org/documentation
[openbaton-github]: http://github.org/openbaton
[openbaton-logo]: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/openBaton.png
[openbaton-mail]: mailto:users@openbaton.org
[openbaton-twitter]: https://twitter.com/openbaton
[tub-logo]: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/tu.png

[bootstrap-tags]: https://github.com/openbaton/bootstrap/releases
[github-nfvo]: https://github.com/openbaton/NFVO
[github-vnfm-generic]: https://github.com/openbaton/generic-vnfm
[github-driver-openstack4j]: https://github.com/openbaton/openstack4j-plugin
[github-vnfm-docker]: https://github.com/openbaton/vnfm-docker-go
[github-driver-docker]: https://github.com/openbaton/go-docker-driver
[github-vnfm-dummy]: https://github.com/openbaton/dummy-vnfm-amqp
[github-driver-test]: https://github.com/openbaton/dummy-vnfm-amqp
[github-zabbix-plugin]: https://github.com/openbaton/zabbix-plugin
[github-ase]: https://github.com/openbaton/autoscaling-engine
[github-nse]: https://github.com/openbaton/network-slicing-engine

[web-rabbitmq]: https://www.rabbitmq.com/
[web-mysql]: https://www.mysql.com/
[web-zabbix]: https://www.zabbix.com/
[zabbix-config]: utils/zabbix/README.mds