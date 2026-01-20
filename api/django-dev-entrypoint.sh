#!/bin/bash

sh django-base-entrypoint.sh

echo "Updating sample data in fixtures"
python scripts/update_dev_data.py

echo "Loading data from fixtures"
python manage.py loaddata fixtures.json

echo "Starting dev server"
python manage.py runserver 0.0.0.0:8000
