#!/bin/bash

sh django-base-entrypoint.sh

echo "Starting prod server"
gunicorn --workers 3 --bind 0.0.0.0:8000 nvdnew.wsgi
