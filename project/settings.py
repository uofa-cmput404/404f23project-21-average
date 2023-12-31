"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import datetime
from pathlib import Path
import os
import dotenv
import dj_database_url
# import cloudinary 
# import cloudinary.uploader 
# import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

SECRET_KEY = os.environ.get("SECRET_KEY")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "django.contrib.sites",
    'django.contrib.staticfiles',
    'socialDistribution',
    'rest_framework',
    'django.contrib.admindocs',
    'drf_spectacular',
    "rest_framework.authtoken",
    'rest_framework_simplejwt',
    "authentication.apps.AuthenticationConfig",
    "allauth",
    "allauth.account",
    "dj_rest_auth",
    "corsheaders",
    'allauth.socialaccount',
    "dj_rest_auth.registration",
    # 'django.contrib.postgres',
    # 'django_postgres_extensions'
    # 'cloudinary_storage',
    # 'cloudinary',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'allauth.account.middleware.AccountMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

MEDIA_URL = '/media/'  # or any prefix you choose
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.PageNumberPagination',
    "PAGE_SIZE": 5,
    'PAGINATE_BY_PARAM': 'size',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    "DEFAULT_PERMISSION_CLASSES": ['rest_framework.permissions.AllowAny'],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

JWT_AUTH = {
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 0,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=86400),
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7)
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'social-auth-token',
    'JWT_AUTH_REFRESH_COOKIE': 'social-auth-refresh-token',
}

SITE_ID = 1  # make sure SITE_ID is set

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']

DEBUG = True
ALLOWED_HOSTS = ['cmput-average-21.herokuapp.com', '127.0.0.1', 'localhost:8000', 'frontend-21-average.herokuapp.com',
                 'frontend-21-average-f45e3b82895c.herokuapp.com', 'cmput-average-21-b54788720538.herokuapp.com', '127.0.0.1:8000',
                 'vibely-23b7dc4c736d.herokuapp.com', 'cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com',
                 'second-instance-a06a2b03061a.herokuapp.com' ]

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    'https://frontend-21-average.herokuapp.com',
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    'https://cmput-average-21.herokuapp.com',
    'http://frontend-21-average.herokuapp.com',
    'https://frontend-21-average-f45e3b82895c.herokuapp.com',
    'https://cmput-average-21-b54788720538.herokuapp.com',
    
    # teams
    'https://vibely-23b7dc4c736d.herokuapp.com',
    'https://second-instance-a06a2b03061a.herokuapp.com',
    'https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com',
    'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com'
]

SPECTACULAR_SETTINGS = {
    'TITLE': '21 Average Social Distribution API',
    'DESCRIPTION': 'Social Distribution API for 21 Average',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_COERCE_PATH_PK_SUFFIX': True,
    'COMPONENT_SPLIT_REQUEST': True
    # OTHER SETTINGS
}

AUTH_USER_MODEL = 'socialDistribution.Author'
ACCOUNT_EMAIL_VERIFICATION = 'none'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# REST_AUTH_SERIALIZERS = {
#     'REGISTER_SERIALIZER': 'authentication.serializers.CustomRegisterSerializer'
# }

CONNECTED = ["vibely", "CtrlAltDefeat", "socialSync"]
DEFAULT_AUTHORS = ["string", "itachi", "metroboomin", "21savage", ]
DEFAULT_AUTHORS_PASSWORD = "string"
BASEHOST = os.environ.get("BASE_URL")
