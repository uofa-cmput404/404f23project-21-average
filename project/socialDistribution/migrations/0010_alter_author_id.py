# Generated by Django 4.2.4 on 2023-10-30 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0009_remove_author_profileimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
