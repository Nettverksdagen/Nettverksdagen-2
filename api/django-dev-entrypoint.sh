#!/bin/bash

sh django-base-entrypoint.sh

# Copy fixtures template to working file if it doesn't exist
if [ ! -f nvdagen/fixtures/fixtures.json ]; then
    echo "Creating fixtures from template..."
    cp nvdagen/fixtures/fixtures.template.json nvdagen/fixtures/fixtures.json
fi

echo "Updating sample data in fixtures"
python scripts/update_dev_data.py

echo "Loading data from fixtures"
python manage.py loaddata nvdagen/fixtures/fixtures.json

echo "Starting dev server"
python manage.py runserver 0.0.0.0:8000
