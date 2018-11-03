#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "Applying database migrations"
python3 manage.py migrate

echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000
