# Open Baton via Docker Compose
## System Requirements
You will need:
- [Docker](https://www.docker.com/community-edition#/download) (>=17.06)
- [Docker Compose](https://docs.docker.com/compose/install/) (>=1.14)
- A checkout of this repository

## Simple deploy
Change into the directory containing the composition YAML files and issue [up](https://docs.docker.com/compose/reference/up/) command. It is important that you set the handed over env variable `HOST_IP` to the reachable IP of your workstation so that deployed VM's can reach the generic VNFM.

You can choose to issue a simple curl loop to check if the orchestrator is up and/or check on the logged output of e.g. the orchestrator. When the deploy is done, you can reach the NFVO's dashboard with your webbrowser at http://localhost:8080
```bash
$ cd bootstrap/distribution/docker/compose
$ env HOST_IP=$YOUR_LOCAL_IP docker-compose -f min_nomysql-compose.yml up -d
$ # until curl -sSf --stderr /dev/null http://localhost:8080; do printf '.' && sleep 5;done
$ # docker logs -f compose_nfvo_1
```

## Related commands
To list all running containers execute:
```bash
$ docker ps
CONTAINER ID        IMAGE                                            COMMAND                  CREATED             STATUS                         PORTS                                                                                        NAMES
9dab845e3048        openbaton/vnfm-generic:latest                    "java -jar /vnfm-g..."   31 seconds ago      Up 3 seconds                                                                                                                compose_vnfm-generic_1
62890a2918b5        openbaton/plugin-vimdriver-test:latest           "sh -c 'java -jar ..."   37 seconds ago      Restarting (1) 2 seconds ago                                                                                                compose_plugin-vimdriver-test_1
43062dd707b9        openbaton/plugin-vimdriver-openstack-4j:latest   "sh -c 'java -jar ..."   37 seconds ago      Up Less than a second                                                                                                       compose_plugin-vimdriver-openstack-4j_1
92dfd7baa5d8        openbaton/nfvo:latest                            "java -jar /nfvo.j..."   41 seconds ago      Up 37 seconds                  0.0.0.0:8080->8080/tcp, 8443/tcp                                                             compose_nfvo_1
03c96f100235        rabbitmq:3-management-alpine                     "docker-entrypoint..."   25 minutes ago      Up 25 minutes                  4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp   compose_rabbitmq_broker_1
```

To attach to one of the running containers with an interactive shell:
```bash
$ docker exec -ti compose_nfvo_1 sh
/ #
```

To attach to the logs of a running container (drop the -f to only dump "what-is"):
```bash
$ docker logs -f compose_nfvo_1
[...]
```

To dispose a deployment:
```bash
$ cd bootstrap/distribution/docker/compose
$ docker-compose -f min_nomysql.yml down
WARNING: The HOST_IP variable is not set. Defaulting to a blank string.
WARNING: The ZABBIX_IP variable is not set. Defaulting to a blank string.
Stopping compose_plugin-vimdriver-openstack-4j_1 ... done
Stopping compose_vnfm-dummy-rest_1 ... done
Stopping compose_vnfm-dummy-amqp_1 ... done
Stopping compose_plugin-vimdriver-test_1 ... done
Stopping compose_vnfm-generic_1 ... done
Stopping compose_nfvo_1 ... done
Stopping compose_rabbitmq_broker_1 ... done
Removing compose_plugin-vimdriver-openstack-4j_1 ... done
Removing compose_vnfm-dummy-rest_1 ... done
Removing compose_vnfm-dummy-amqp_1 ... done
Removing compose_plugin-vimdriver-test_1 ... done
Removing compose_vnfm-generic_1 ... done
Removing compose_nfvo_1 ... done
Removing compose_rabbitmq_broker_1 ... done
Removing network compose_default
```

To restart only a single service, e.g. after changing ENV variables of the openstackplugin in the compose file:
```bash
$ docker-compose -f min-compose.yml up -d --no-deps plugin-vimdriver-openstack-4j
Recreating compose_plugin-vimdriver-openstack-4j_1
```
## Available scenarios
- min-compose: Containing NFVO, vnfm-generic, vnfm-dummy-amqp, test- and openstack-plugin, MySQL, RabbitMQ
- min_nomysql-compose: As above, but without MySQL but rather the in-memory database

## Further configuration
Without further configuration docker-compose will use the images build on [Docker Hub](https://hub.docker.com/r/openbaton/) with the `latest` tag, which are build from the last pushes to the respective `master` branch. Check the repo for available tagged releases and replace the `latest` tag accordingly.

If you have a installed and configured Zabbix2 or Zabbix3 server running and want Open Baton to automatically add monitoring capabilities to the deployed NSR's, you can set `ZABBIX_IP` just as `HOST_IP` on executing the `up` command. So the deploy would then look like
```bash
$ env HOST_IP=$YOUR_LOCAL_IP ZABBIX_IP=$YOUR_ZABBIX_SERVER_IP docker-compose -f min_nomysql-compose.yml up -d
```
