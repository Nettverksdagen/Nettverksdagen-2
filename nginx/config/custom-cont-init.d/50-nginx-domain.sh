#!/bin/bash
envsubst '${DOMAIN}' < /config/nginx/site-confs/default.conf.template > /config/nginx/site-confs/default.conf
