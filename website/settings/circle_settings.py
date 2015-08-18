from __future__ import unicode_literals, absolute_import

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
        "NAME": "circle_test",
        # Not used with sqlite3.
        "USER": "ubuntu",
        # Not used with sqlite3.
        "PASSWORD": "",
    }
}


##########
# DJANGO #
##########

DEBUG = True

SECRET_KEY = 'toot toot toot'