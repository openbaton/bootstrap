# Create the Open Baton base docker image
FROM openbaton/rabbitmq
MAINTAINER Open Baton <dev@openbaton.org>

# Setting this variables allow to install Open Baton through the debian package but respectively skipping:
#  - the interactive installation (the default values will be selected and both the 'test' and 'openstack' VIM Drivers Plugins will be downloaded)
#  - the RabbitMQ configuration (which need to be preconfigured - this is done in the 'openbaton/rabbitmq' Base Docker image)
#  - the "OS-based service starting" (the starting of the NFVO and the GVNFM is managed in this Docker file)
ENV DEBIAN_FRONTEND noninteractive
ENV CONFIGURE_RABBITMQ_FOR_OPENBATON false
ENV OPENBATON_AUTOSTART false

ENV RABBITMQ_BROKERIP=localhost

# Adding Open Baton repository and installing NFVO and GVNFM
RUN wget -O - http://get.openbaton.org/keys/public.gpg.key | apt-key add -
RUN echo "deb http://get.openbaton.org/repos/apt/debian/ stable main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y --force-yes \
    openbaton-nfvo \
    openbaton-gvnfm

# Installing the OpenStack VIM Driver Plugin
RUN cd /usr/lib/openbaton/plugins/ && wget http://get.openbaton.org/plugins/1.0.2-liberty/openstack-plugin-1.0.2-liberty.jar

# Supervisor installation (allow to run multiple services in a Docker container)
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080 8443 5672 15672

CMD ["/usr/bin/supervisord"]
