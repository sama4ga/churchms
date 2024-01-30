"""
Django settings for churchms project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

if DEBUG:
  from dotenv import load_dotenv
  load_dotenv(".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


ALLOWED_HOSTS = ['*']

# FORM SUBMISSION
# Comment out the following line and place your railway URL, and your production URL in the array.
# CSRF_TRUSTED_ORIGINS = ["*"]


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'church.apps.ChurchConfig',
    'station.apps.StationConfig',
    'society.apps.SocietyConfig',
    'pious_society.apps.PiousSocietyConfig',
    'lay_apostolate.apps.LayApostolateConfig',
    'other_group.apps.OtherGroupConfig',
    'council.apps.CouncilConfig',
    'parishioner.apps.ParishionerConfig',
    'priest.apps.PriestConfig',
    'organisation.apps.OrganisationConfig',
    'setting.apps.SettingConfig',
    'baptism.apps.BaptismConfig',
    'communion.apps.CommunionConfig',
    'confirmation.apps.ConfirmationConfig',
    'matrimony.apps.MatrimonyConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'rest_framework',
    'widget_tweaks',
    # 'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'churchms.urls'

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

WSGI_APPLICATION = 'churchms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


if DEBUG:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
      'CONN_MAX_AGE': 3600
    }
  }
  
  EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
  EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
  # EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': os.environ.get("PGDATABASE"),
      'USER': os.environ.get("PGUSER"),
      'PASSWORD': os.environ.get("PGPASSWORD"),
      'HOST': os.environ.get("PGHOST"),
      'PORT': os.environ.get("PGPORT"),
      'CONN_MAX_AGE': 3600
    }
  }

  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER") 
  EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')


CONN_HEALTH_CHECKS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "file": {
            "level": os.environ.get("DJANGO_LOG_LEVEL"),
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL"),
            "propagate": True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
      "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos' # 'Africa/Lagos' 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'users-login'
LOGIN_REDIRECT_URL = 'church-home'

DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")   #config['EMAIL_USER']
SERVER_EMAIL = os.environ.get("EMAIL_HOST_USER") 
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CSRF_TRUSTED_ORIGINS = [
#     'https://your-base-domain'
# ]
