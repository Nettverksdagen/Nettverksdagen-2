#!/bin/bash

./backup.sh
docker-compose -f docker-compose-prod.yml build

docker-compose -f docker-compose-prod.yml stop nginx
yes | docker-compose -f docker-compose-prod.yml rm nginx
docker volume rm nettverksdagen-2_frontend-files
docker-compose -f docker-compose-prod.yml up --no-deps -d 
yes | docker-compose -f docker-compose-prod.yml rm frontend
