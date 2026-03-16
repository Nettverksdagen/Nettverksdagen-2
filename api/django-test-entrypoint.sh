#!/bin/bash
# Exit upon any failure
set -e

sh django-base-entrypoint.sh

echo "Loading data from fixtures"
python manage.py loaddata nvdagen/fixtures/fixtures.template.json

echo "Running tests"
python manage.py test test

