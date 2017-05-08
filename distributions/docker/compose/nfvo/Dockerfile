# Create the OpenBaton base docker image
FROM openbaton/rabbitmq
MAINTAINER Open Baton <dev@openbaton.org>

# Setting this variables allow to install Open Baton through the debian package but respectively skipping:
#  - the RabbitMQ configuration (which need to be preconfigured - this is done in the 'openbaton/rabbitmq' Base Docker image)
#  - the interactive installation (the default values will be selected and both the 'test' and 'openstack' VIM Drivers Plugins will be downloaded)
#  - the "OS-based service starting" (the starting of the NFVO is managed in this Docker file)
ENV CONFIGURE_RABBITMQ_FOR_OPENBATON false
# Already set in the configuration file
#ENV openbaton_installation_manner noninteractive
#ENV openbaton_component_autostart false # needs to be lower case to not be overwritten by the bootstrap

ENV RABBITMQ_BROKERIP=localhost

# Adding Open Baton repository and installing the NFVO
COPY bootstrap-config-file /tmp/
RUN wget http://get.openbaton.org/bootstrap && chmod +x bootstrap && ./bootstrap release --config-file=/tmp/bootstrap-config-file

# Supervisor
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080 8443 5672 15672

CMD ["/usr/bin/supervisord"]
