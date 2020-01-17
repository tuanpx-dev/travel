"""
Django settings for travel project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ad3idydg74=4t4!@o5#1uf1jipbld*hqx+eua_0!n^el*cvd+r'

EXPIRED_TOKEN_TIME = 7 * 24 * 3600  # 7 day

IS_PRODUCTION = 'INFO'
IS_STAGING = 'DEBUG'
IS_TESTING = 'ERROR'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework_swagger',
    'rest_framework',
    'apps.users',
    'apps.category',
    'apps.questions',
    'apps.answers',
    'apps.comments',
    'apps.area',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'travel.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'travel.urls'
AUTH_USER_MODEL = 'users.User'

CORS_ORIGIN_ALLOW_ALL = True

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

WSGI_APPLICATION = 'travel.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travel_db',
        'USER': 'travel_user',
        'PASSWORD': 'travel_user',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


def __get_log_level():
    if IS_TESTING:
        return 'ERROR'
    if IS_PRODUCTION:
        return 'INFO'
    else:
        return 'DEBUG'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s: %(name)s:%(lineno)d %(process)d %(thread)d [%(levelname)s] - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/backend.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 100,
            'formatter': 'verbose',
        },
        'sqllog': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/sql.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 100,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['sqllog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# URL get profile on facebook
URL_GET_ID_FACEBOOK = "https://graph.facebook.com/me?access_token="


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (),
}

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

# setting path media
STATIC_URL = '/files/'
MEDIA_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

# domain server
DOMAIN_SERVER = 'http://34.87.111.216:8000/'
