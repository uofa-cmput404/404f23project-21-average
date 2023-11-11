import os
from .base import *
import environ

env = environ.Env()
environ.Env.read_env()


DEBUG = False
DATABASES = {
    'default': {
       "ENGINE": 'django.db.backends.postgresql',
        "NAME": 'SocialDistribution',
        "USER": 'postgres',
        "PASSWORD": 'postgres',
        # "HOST": env("SQL_HOST", "localhost"),
        # "PORT": env("SQL_PORT", "3306"),
    }
}

ALLOWED_HOSTS = ['avergae-21-b951939c31ad.herokuapp.com',
                 'localhost', '127.0.0.1', 'localhost:3000']