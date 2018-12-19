#!/bin/bash

sh django-base-entrypoint.sh

echo "Starting prod server"
gunicorn --bind 0.0.0.0:8000 nvdnew.wsgi
