from __future__ import unicode_literals, absolute_import
import os
import logging

logger = logging.getLogger(__name__)


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "lantasy",
        # Not used with sqlite3.
        "USER": os.environ['DJANGO_DB_USER'],
        # Not used with sqlite3.
        "PASSWORD": os.environ['DJANGO_DB_PASS'],
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


##########
# DJANGO #
##########

DEBUG = True

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']