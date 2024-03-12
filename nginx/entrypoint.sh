#!/bin/bash
set -e
sed -i "s|{{APP_HOST}}|$APP_HOST|;s|{{NGINX_PROXY}}|$NGINX_PROXY|" \
        /etc/nginx/conf.d/default.conf
cat /etc/nginx/conf.d/default.conf
exec "$@"