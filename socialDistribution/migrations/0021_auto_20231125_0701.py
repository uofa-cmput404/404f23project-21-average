# Generated by Django 4.2.4 on 2023-11-25 07:01

from django.db import migrations
import logging
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


def generate_superuser(apps, schema_editor):
    USERNAME = 'admin'
    PASSWORD = 'admin'
    EMAIL = 'nabi1@ualberta.ca'

    user = get_user_model()

    if not user.objects.filter(username=USERNAME, email=EMAIL).exists():
        logger.info("Creating new superuser")
        admin = user.objects.create_superuser(
           username=USERNAME, password=PASSWORD, email=EMAIL, type="admin"
        )
        admin.save()
    else:
        logger.info("Superuser already created!")


def generate_nodes(apps, schema_editor):
    user = get_user_model()
    
    for connectedNode in settings.CONNECTED:
        if not user.objects.filter(username=connectedNode).exists():
            logger.info("Creating new node user")
            node = user.objects.create_user(
            username=connectedNode, password=settings.DEFAULT_AUTHORS_PASSWORD, type="node", 
            )

            node.save()
        else:
            logger.info("Node user already created!")


def generate_default_user(apps, schema_editor):
    user = get_user_model()

    for default_username in settings.DEFAULT_AUTHORS:
        if not user.objects.filter(username=default_username).exists():
            logger.info("Creating new default user")
            default_user = user.objects.create_user(
                username=default_username, password=settings.DEFAULT_AUTHORS_PASSWORD, host=settings.BASEHOST,
                type="author", displayName=default_username
            )
            default_user.save()
        else:
            logger.info("Default user already created!")


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0020_rename_parentpost_comment_post'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
        migrations.RunPython(generate_nodes),
        migrations.RunPython(generate_default_user),
    ]
