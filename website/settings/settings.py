from __future__ import absolute_import, unicode_literals
import os
import platform
from django.utils.translation import ugettext_lazy as _

######################
# CARTRIDGE SETTINGS #
######################

SHOP_DISCOUNT_FIELD_IN_CART = True
SHOP_DISCOUNT_FIELD_IN_CHECKOUT = True

# SHOP_CATEGORY_USE_FEATURED_IMAGE = True

# Set an alternative OrderForm class for the checkout process.
# SHOP_CHECKOUT_FORM_CLASS = 'cartridge.shop.forms.OrderForm'


# If True, the checkout process is split into separate billing/shipping and payment steps.
# SHOP_CHECKOUT_STEPS_SPLIT = True

SHOP_CHECKOUT_STEPS_CONFIRMATION = True

if platform.system() == 'Windows':
    SHOP_CURRENCY_LOCALE = 'english-can'
else:
    SHOP_CURRENCY_LOCALE = 'en_CA.utf8'

SHOP_HANDLER_ORDER = 'website.apps.salesbro.checkout.salesbro_order_handler'
SHOP_HANDLER_TAX = 'website.apps.salesbro.checkout.salesbro_tax_handler'

SHOP_HANDLER_PAYMENT = 'cartridge_stripe.payment_handler'
SHOP_CHARGE_CURRENCY = 'cad'
SHOP_ORDER_FROM_EMAIL = DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'noreply@lantasy.com'
SHOP_ORDER_EMAIL_SUBJECT = 'LANtasy Order Invoice'
SHOP_CARD_TYPES = 'Mastercard', 'Visa', 'Amex'

SHOP_CHECKOUT_ACCOUNT_REQUIRED = True

SHOP_DEFAULT_SHIPPING_VALUE = 0

SHOP_USE_WISHLIST = False

ZEBRA_ENABLE_APP = True

######################
# MEZZANINE SETTINGS #
######################

ACCOUNTS_VERIFICATION_REQUIRED = True

USE_MODELTRANSLATION = False


########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.lantasy.com',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# Supported languages
LANGUAGES = (
    ('en', _('English')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

AUTHENTICATION_BACKENDS = ('mezzanine.core.auth_backends.MezzanineBackend',)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # DB name or path to database file if using sqlite3.
        'NAME': 'lantasy',
        # Not used with sqlite3.
        'USER': os.getenv('DJANGO_DB_USER'),
        # Not used with sqlite3.
        'PASSWORD': os.getenv('DJANGO_DB_PASS'),
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}


#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')


STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'apps/themebro/static/common'),)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + 'media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = 'website.urls'

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'themes/default/templates'),)


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    # --Theme--
    'website.apps.themebro',

    # --Django--
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    # --Mezzanine--
    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.pages',
    'mezzanine.blog',
    'mezzanine.forms',
    'mezzanine.galleries',
    # 'mezzanine.twitter',
    'mezzanine.accounts',
    # 'mezzanine.mobile',

    # --Cartridge--
    'cartridge_stripe',
    'cartridge.shop',
    'zebra',
    'django_mailgun',

    # --Debug--
    'django_extensions',
    'debug_toolbar',

    # --Core--
    'website.apps.eventbro',
    'website.apps.salesbro',
    'website.apps.badgebro',

    # --Utils--
    'django_cleanup',
    'sorl.thumbnail',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'mezzanine.conf.context_processors.settings',
    'mezzanine.pages.context_processors.page',
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    'mezzanine.core.middleware.UpdateCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    # Uncomment if using internationalisation or localisation
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'cartridge.shop.middleware.ShopMiddleware',
    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    'debug_toolbar',
    'django_extensions',
    'compressor',
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
NEVERCACHE_KEY = os.getenv('DJANGO_NEVERCACHE_KEY')

# Stripe
STRIPE_SECRET = os.getenv('DJANGO_STRIPE_SECRET')
STRIPE_PUBLISHABLE = os.getenv('DJANGO_STRIPE_PUBLISHABLE')

# Mailgun
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.getenv('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = os.getenv('MAILGUN_SERVER_NAME')

# Thumbnails
THUMBNAIL_CACHE_TIMEOUT = 3600 * 24 * 120

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from website.settings.local_settings import *
except ImportError as e:
    pass


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(PROJECT_ROOT, '../../logs/django.log'),
        #     'formatter': 'verbose'
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
