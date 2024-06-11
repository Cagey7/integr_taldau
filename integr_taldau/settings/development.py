import os
from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "integr_taldau_development1",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
