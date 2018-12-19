#!/bin/bash

sh django-base-entrypoint.sh

echo "Starting dev server"
python manage.py runserver 0.0.0.0:8000
