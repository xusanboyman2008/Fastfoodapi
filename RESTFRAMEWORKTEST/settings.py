"""
Django settings for RESTFRAMEWORKTEST project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import datetime
from pathlib import Path
import dj_database_url
import AUTH_USER
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNwING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-)wx((d2@ja+3gieh#7ypiyjli7z_748=bdhzs38dzkc8_7g@cx'
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = ['django.contrib.auth',    'corsheaders',
 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.admin', 'django.contrib.messages', 'django.contrib.staticfiles', 'api.apps.ApiConfig',
                  'rest_framework', 'rest_framework.authtoken', 'AUTH_USER']

AUTH_USER_MODEL = 'AUTH_USER.User'

EXPIRING_TOKEN_LIFESPAN = datetime.timedelta(days=25)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Temporarily comment out
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Temporarily comment out
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = ['*']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOW_HEADERS = ['authorization', 'content-type', ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.ExpiringTokenAuthentication',  # ensure this class is correct
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
LOGIN_REDIRECT_URL = '/api/'

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
     'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                        'django.template.context_processors.request',
                                        'django.contrib.auth.context_processors.auth',
                                        'django.contrib.messages.context_processors.messages', ], }, }, ]

WSGI_APPLICATION = 'RESTFRAMEWORKTEST.wsgi.application'

ROOT_URLCONF = 'RESTFRAMEWORKTEST.urls'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3', }}
database_url = os.environ.get('DATABASE_URL')
# database_url = 'postgresql://xsanboyman_user:k5vNyotJFqeRMpuCXQCHf0GSsZJIjXZS@dpg-ctv0os5ds78s738lm9u0-a.oregon-postgres.render.com/xsanboyman'
DATABASES['default'] = dj_database_url.parse(database_url)
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
