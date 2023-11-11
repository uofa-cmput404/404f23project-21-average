"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise
from whitenoise import WhiteNoise
import environ

environ.Env.read_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.production')

application = get_wsgi_application()
pplication = WhiteNoise(application)
