FROM mongo

USER root

RUN apt-get update && \
    apt-get install -y wget gnupg && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add >
    echo "deb http://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multive>
    apt-get update && \
    apt-get install -y mongodb-org-shell && \
    rm -rf /var/lib/apt/lists/*

