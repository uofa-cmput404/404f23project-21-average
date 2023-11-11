import os
from .base import *
import environ

env = environ.Env()
environ.Env.read_env()


DEBUG = False
DATABASES = {
    'default': {
       "ENGINE": env("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env("SQL_DATABASE", os.path.join(BASE_DIR, 'db.sqlite3')),
        "USER": env("SQL_USER", "myuser"),
        "PASSWORD": env("SQL_PASSWORD", "myuserpassword"),
        "HOST": env("SQL_HOST", "localhost"),
        "PORT": env("SQL_PORT", "3306"),
    }
}

ALLOWED_HOSTS = ['avergae-21-b951939c31ad.herokuapp.com',
                 'localhost', '127.0.0.1', 'localhost:3000']