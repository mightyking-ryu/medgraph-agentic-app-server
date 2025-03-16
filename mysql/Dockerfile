FROM mysql:8.0.41-debian

COPY ./init-template.sql /docker-entrypoint-initdb.d/init-template.sql
COPY ./init.sh /docker-entrypoint-initdb.d/init.sh

RUN chmod +x /docker-entrypoint-initdb.d/init.sh

ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_DATABASE

ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}

RUN apt-get update && apt-get install -y gettext && \
    /docker-entrypoint-initdb.d/init.sh && \
    apt-get remove -y gettext && apt-get autoremove -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /docker-entrypoint-initdb.d/init.sh /docker-entrypoint-initdb.d/init-template.sql