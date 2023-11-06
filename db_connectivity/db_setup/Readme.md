.env will contain the following:

      MONGO_INITDB_ROOT_USERNAME=
      MONGO_INITDB_ROOT_PASSWORD=
      DB_NAME=
      S3_BUCKET=

**Ensure that the .env file is readable only by the user who will run the script and is not accessible by others, as it contains sensitive information**

      1.install MongoDB using docker -

      build docker image first:

      docker build -t mongodb-with-shell .

      2.run mongodb server using docker container:

      docker-compose up
