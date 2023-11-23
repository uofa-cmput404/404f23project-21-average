# Generated by Django 4.2.4 on 2023-11-23 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0015_connectednode_api_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='owner',
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default='e7bfa565-d3c8-46b8-b321-2ff4d43914ff', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
