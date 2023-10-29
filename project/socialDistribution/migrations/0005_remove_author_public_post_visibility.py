# Generated by Django 4.2.4 on 2023-10-29 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0004_remove_author_comments_remove_author_followers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='public',
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(default='PUBLIC', max_length=255),
            preserve_default=False,
        ),
    ]