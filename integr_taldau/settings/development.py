from .base import *

SECRET_KEY = 'django-insecure-f-cibx#z41@wviy4x-v1qdgt1lj_%0m@^)*g4e+wm$ste-xiv_'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "integr_taldau_development",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "db",
        "PORT": "5432",
    }
}
