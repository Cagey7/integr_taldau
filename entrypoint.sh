#!/bin/bash
set -e

DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@gmail.com"}
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"admin"}
APP_PORT=${APP_PORT:-8000}

if [ "$ENV" = 'DEV' ]; then
    echo "Running Development Server"
    pip install -r requirements/development.txt
    python manage.py migrate --noinput --settings=integr_taldau.settings.development
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --settings=integr_taldau.settings.development || true
    python manage.py runserver 0.0.0.0:$APP_PORT --settings=integr_taldau.settings.development
else
    echo "Running Production Server"
    pip install -r requirements/production.txt
    python manage.py migrate --noinput --settings=integr_taldau.settings.production
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --settings=integr_taldau.settings.production || true
    gunicorn --worker-tmp-dir /dev/shm integr_taldau.wsgi:application --bind "0.0.0.0:${APP_PORT}"
fi
