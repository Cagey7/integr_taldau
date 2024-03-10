#!/bin/bash
APP_PORT=${PORT:-8000}

cd /code/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm integr_taldau.wsgi:application --bind "0.0.0.0:${APP_PORT}"
