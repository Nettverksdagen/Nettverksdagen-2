#!/bin/bash

./backup.sh
git reset --hard origin/master
git pull

yes | docker-compose -f docker-compose-prod.yml rm frontend
docker-compose -f docker-compose-prod.yml build

docker-compose -f docker-compose-prod.yml stop nginx
yes | docker-compose -f docker-compose-prod.yml rm nginx
docker volume rm nettverksdagen-2_frontend-files
docker-compose -f docker-compose-prod.yml up --no-deps -d nginx fileserver api frontend postgres
