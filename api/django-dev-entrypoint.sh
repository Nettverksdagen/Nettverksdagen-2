#!/bin/bash

sh django-base-entrypoint.sh

echo "Loading data from fixtures"
python manage.py loaddata fixtures.json

echo "Starting dev server"
python manage.py runserver 0.0.0.0:8000
