# Create the Open Baton base docker image
FROM openbaton/rabbitmq
MAINTAINER Open Baton <dev@openbaton.org>

# Setting this variables allow to install Open Baton through the debian package but respectively skipping:
#  - the interactive installation (the default values will be selected and both the 'test' and 'openstack' VIM Drivers Plugins will be downloaded)
#  - the RabbitMQ configuration (which need to be preconfigured - this is done in the 'openbaton/rabbitmq' Base Docker image)
#  - the "OS-based service starting" (the starting of the NFVO and the GVNFM is managed in this Docker file)
ENV CONFIGURE_RABBITMQ_FOR_OPENBATON false
ENV openbaton_installation_manner noninteractive
ENV openbaton_component_autostart false # needs to be lower case to not be overwritten by the bootstrap

ENV RABBITMQ_BROKERIP=localhost

# Installing NFVO and GVNFM through the bootstrap
RUN wget http://get.openbaton.org/bootstrap && chmod +x bootstrap && ./bootstrap release

# Supervisor installation (allow to run multiple services in a Docker container)
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080 8443 5672 15672

CMD ["/usr/bin/supervisord"]
