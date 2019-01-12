#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "Entering api dir"
cd api

echo "Applying all database migrations"
python manage.py migrate
