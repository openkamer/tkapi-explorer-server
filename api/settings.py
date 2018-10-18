"""
Django settings for api project.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    'api',
    'corsheaders',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True

INTERNAL_IPS = ['127.0.0.1']  # needed for django-debug-toolbar

# corsheaders
CORS_ORIGIN_ALLOW_ALL = True

# Local settings
# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
from api.local_settings import *


# Logging
LOG_DIR = os.path.join(BASE_DIR, 'log')

LOGFILE_MAXSIZE = 10 * 1024 * 1024

# Number of old log files that are stored before they are deleted
# see https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler
LOGFILE_BACKUP_COUNT = 3

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s::%(funcName)s() (%(lineno)s)]: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'file_django': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': LOGFILE_MAXSIZE,
            'backupCount': LOGFILE_BACKUP_COUNT,
            'formatter': 'verbose'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': LOGFILE_MAXSIZE,
            'backupCount': LOGFILE_BACKUP_COUNT,
            'formatter': 'verbose'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': LOGFILE_MAXSIZE,
            'backupCount': LOGFILE_BACKUP_COUNT,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_django', 'console'],
            'propagate': True,
            'level': 'ERROR',
        },
        'api': {
            'handlers': ['file_debug', 'file_error', 'console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}