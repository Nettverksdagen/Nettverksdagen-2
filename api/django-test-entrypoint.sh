#!/bin/bash
sh django-base-entrypoint.sh

echo "Loading data from fixtures"
python manage.py loaddata fixtures.json

echo "Running tests"
python manage.py test test

