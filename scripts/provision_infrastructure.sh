#!/bin/bash

STATE_BUCKET_NAME="chesscv-tfstate"
export AWS_REGION="eu-central-1"

aws s3 mb s3://"$STATE_BUCKET_NAME"

cd terraform && terraform init && terraform apply -auto-approve