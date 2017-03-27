FROM ubuntu:trusty
MAINTAINER Open Baton <dev@openbaton.org>

# Setting this variables allow to install Open Baton through the debian package but skipping:
#  - the interactive installation (the default values will be selected)
#  - the "OS-based service starting" (the starting of the Generic VNFM is managed in this Docker file)
ENV openbaton_installation_manner noninteractive
ENV OPENBATON_COMPONENT_AUTOSTART false

ENV RABBITMQ_BROKERIP=localhost

RUN apt-get update
RUN apt-get install -y wget

# Adding Open Baton repository and installing the Generic VNFM
RUN wget -O - http://get.openbaton.org/keys/openbaton.public.key | apt-key add -
RUN echo "deb http://get.openbaton.org/repos/openbaton/trusty/release trusty main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y --force-yes \
    openbaton-vnfm-generic


# Supervisor
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5672

CMD ["/usr/bin/supervisord"]
