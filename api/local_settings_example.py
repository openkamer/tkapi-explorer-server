"""
local settings, included in settings.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: Make this unique, and don't share it with anybody.
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, 'dev.sqlite'),                      # Or path to database file if using sqlite3.
    }
}

LANGUAGE_CODE = 'en-US'

TIME_ZONE = "Europe/Amsterdam"

#STATIC_ROOT = '/home/username/webapps/<staticdir>/'
STATIC_ROOT = ''

#STATIC_URL = '//www.domain.com/static/'
STATIC_URL = '/static/'

# TKAPI
TKAPI_ROOT_URL = 'https://gegevensmagazijn.tweedekamer.nl/OData/v3/1.0/'
TKAPI_USER = ''
TKAPI_PASSWORD = ''
