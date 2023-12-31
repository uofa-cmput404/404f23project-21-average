# Generated by Django 4.2.4 on 2023-11-18 02:23

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=255)),
                ('displayName', models.CharField(max_length=255)),
                ('github', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(max_length=255)),
                ('published', models.DateTimeField()),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectedNode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('teamName', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('origin', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('contentType', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('published', models.DateTimeField(default=datetime.datetime.now)),
                ('categories', models.TextField(blank=True, null=True)),
                ('count', models.IntegerField(default=0)),
                ('visibility', models.CharField(default='PUBLIC', max_length=255)),
                ('unlisted', models.BooleanField(default=False)),
                ('imageOnlyPost', models.BooleanField(default=False)),
                ('image_link', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('published', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialDistribution.post')),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=255)),
                ('from_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_author', to=settings.AUTH_USER_MODEL)),
                ('to_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=255)),
                ('from_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_author_follow', to=settings.AUTH_USER_MODEL)),
                ('to_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_author_follow', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('published', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialDistribution.comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='parentPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialDistribution.post'),
        ),
    ]
