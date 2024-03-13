from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "integr_taldau_test",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "db",
        "PORT": "5432",
    }
}
