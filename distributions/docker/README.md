# Open Baton via Docker 

To have a running standalone Open Baton Docker container type the following commands:

```bash
sudo docker pull openbaton/standalone
sudo docker run -d -h openbaton-rabbitmq -p 8080:8080 -p 5672:5672 -p 15672:15672 -p 8443:8443 -e RABBITMQ_BROKERIP=<RabbitMQ IP> openbaton/standalone
```

***NOTE*** *- With the above commands you will download and run the latest Open Baton version. In case you would like to try some previous versions you can see which ones
  are available from [this][reference-to-op-repo-on-public-docker-hub] list*

***VERY IMPORTANT NOTE*** *- You should put as input for the RABBITMQ_BROKERIP the RabbitMQ IP making sure that this IP can be
  reached by external components (VMs, or host where will run other VNFMs) otherwise you will have runtime issues.
  In particular, you should select the external IP of your host on top of which the docker container is running**

After running the container you should see as output an alphanumeric string (which represents the Open Baton container's full ID running) similar to the following:

```bash
cfc4a7fb23d02c47e25b447d30f6fe7c0464355a16ee1b02d84657f6fba88e07
```

To verify that the container is running you can type the following command:

```bash
sudo docker ps -a
```

which output should be similar to the following:

```bash
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS                   PORTS                                                                                              NAMES
cfc4a7fb23d0        openbaton/standalone   "/usr/bin/supervisord"   49 seconds ago      Up 49 seconds            0.0.0.0:5672->5672/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:8443->8443/tcp, 0.0.0.0:15672->15672/tcp   admiring_lalande
```

To connect to the running container containing Open Baton you can type the following command:

```bash
sudo docker exec -ti cfc4a7fb23d02c47e25b447d30f6fe7c0464355a16ee1b02d84657f6fba88e07 bash
```

After few minutes the Open Baton NFVO should be started, then you can open a browser and go on localhost:8080.
To log in, the default credentials for the administrator user are:
* user: admin
* password: openbaton 

To stop and delete the running container you can type respectively the following commands:

```bash
sudo docker stop cfc4a7fb23d02c47e25b447d30f6fe7c0464355a16ee1b02d84657f6fba88e07
sudo docker rm cfc4a7fb23d02c47e25b447d30f6fe7c0464355a16ee1b02d84657f6fba88e07
```

## Custom configuration files
The NFVO and Generic VNFM configurations can be tweaked using Docker's builtin _volume bind_ feature, accessible
while starting the container using the **-v** parameter. 
This is expecially useful if you wish to control the logging verbosity of the NFVO.

```bash
sudo docker run -d -h openbaton-rabbitmq -p 8080:8080 -p 5672:5672 -p 15672:15672 -p 8443:8443 -e RABBITMQ_BROKERIP=<RabbitMQ IP> -v /path/to/openbaton-nfvo.properties:/etc/openbaton/openbaton-nfvo.properties openbaton/standalone
```

[reference-to-op-repo-on-public-docker-hub]:https://hub.docker.com/r/openbaton/standalone/tags/
