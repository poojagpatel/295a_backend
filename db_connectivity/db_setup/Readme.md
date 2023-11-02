.env will contain the following:

MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
DB_NAME=
S3_BUCKET=

Ensure that the .env file is readable only by the user who will run the script and is not accessible by others, as it contains sensitive information:

1.install mongodb using docker -

build docker image first:

docker build -t mongodb-with-shell .

2.run mongodb server using docker container:

docker-compose up

cron script setting:

1.give necessary permissions:

chmod +x backup_script.sh

2. Schedule the Backup with Cron
   Open the crontab configuration file:

   crontab -e

Add the following line to schedule the script to run every Monday at 12 PM:

    MAILTO="your@email.com"
    0 12 \* \* 1 /path/to/backup_mongodb.sh

This cron job will execute the backup_mongodb.sh script every Monday at 12:00 PM. it will also mail once this cron execution done.
