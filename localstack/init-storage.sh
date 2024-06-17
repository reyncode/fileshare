#!/bin/bash

if [ -z "$FILE_BUCKET_NAME" ]; then
  FILE_BUCKET_NAME=file-bucket
fi

# Create the initial bucket for file storage
awslocal s3api create-bucket --bucket $FILE_BUCKET_NAME

# Apply the CORS configuration
awslocal s3api put-bucket-cors --bucket $FILE_BUCKET_NAME --cors-configuration file:///config/cors-config.json
