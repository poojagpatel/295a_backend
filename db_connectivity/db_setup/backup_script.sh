#!/bin/bash

# Load environment variables
export $(grep -v '^#' .env | xargs)

# MongoDB container name
MONGO_CONTAINER="mongodb"

# Backup file name
BACKUP_NAME="mongodb_backup_$(date +%Y%m%d_%H%M%S).gz"

# Dump and compress MongoDB database
docker exec $MONGO_CONTAINER mongodump --archive --gzip --db $DB_NAME --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --out /data/db/$BACKUP_NAME

# Copy the backup to the local file system
docker cp $MONGO_CONTAINER:/data/db/$BACKUP_NAME .

# Upload the backup to S3
aws s3 cp $BACKUP_NAME s3://$S3_BUCKET/$BACKUP_NAME

# Optional: Remove the local backup file
rm $BACKUP_NAME

echo "Backup completed and uploaded to S3"
