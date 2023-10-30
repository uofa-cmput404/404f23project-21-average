# Generated by Django 4.2.4 on 2023-10-30 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0008_post_image_post_image_link_post_shared_with_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='profileImage',
        ),
        migrations.RemoveField(
            model_name='post',
            name='shared_with_friends',
        ),
        migrations.AddField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
