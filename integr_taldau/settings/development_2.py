import os
from .development import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'readuser',
        'PASSWORD': 'readonlyuser1234',
        'HOST': '5.63.114.131',
        'PORT': '5432'
    }
}