# -*- coding: utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os



DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_USE_DEVSERVER = DEBUG

ADMINS = (
    ('Support', 'denis.churkin+luggage@gmail.com'),
)

SERVER_EMAIL = 'support@onpy.ru'
DEFAULT_FROM_EMAIL = 'support@onpy.ru'
PINAX_STRIPE_INVOICE_FROM_EMAIL = 'no-reply@luggary.com'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

from django.utils.translation import ugettext_lazy as _
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

PARLER_DEFAULT_LANGUAGE = 'en-us'

PARLER_LANGUAGES = {
    1: (
        {'code': 'en'},
        {'code': 'es'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': True,
    }
}

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'luggage.middleware.CurrencyFromLocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'constance.context_processors.config',
    'luggage.context_processors.context_params',
    'currencies.context_processors.currencies',
)

OPENEXCHANGERATES_APP_ID = "f983ad0faa03448c9201f71ee96bf88c"

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.admindocs',
    'post_office',
    'django_extensions',
    'easy_thumbnails',
    'parsley',
    'compressor',
    'constance',
    'constance.backends.database',
    'luggage',
    'parler',

    #'ajax_select',
    'cities_light',
    'cities',
    'currencies',
    'pinax.stripe',

    'reversion', # after core
)

# Localized names will be imported for all ISO 639-1 locale codes below.
# 'und' is undetermined language data (most alternate names are missing a lang tag).
# See download.geonames.org/export/dump/iso-languagecodes.txt
# 'LANGUAGES' will match your language settings, and 'ALL' will install everything
CITIES_LOCALES = ['en', 'LANGUAGES']

# Postal codes will be imported for all ISO 3166-1 alpha-2 country codes below.
# You can also specificy 'ALL' to import all postal codes.
# See cities.conf for a full list of country codes. 'ALL' will install everything.
# See download.geonames.org/export/dump/countryInfo.txt
CITIES_POSTAL_CODES = ['ALL']

# List of plugins to process data during import
CITIES_PLUGINS = [
    'cities.plugin.postal_code_ca.Plugin',  # Canada postal codes need region codes remapped to match geonames
    'cities.plugin.reset_queries.Plugin',  # plugin that helps to reduce memory usage when importing large datasets (e.g. "allCountries.zip")
]

# Import cities without region (default False)
CITIES_IGNORE_EMPTY_REGIONS = True

# This setting may be specified if you use 'cities.plugin.reset_queries.Plugin'
CITIES_PLUGINS_RESET_QUERIES_CHANCE = 1.0 / 1000000

AUTH_USER_MODEL = 'luggage.User'
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en',]

LOGOUT_URL = '/'

# grappelli config
GRAPPELLI_ADMIN_TITLE = 'Get Luggage Admin'


# easy-thumbnails config
THUMBNAIL_DEBUG = DEBUG

THUMBNAIL_ALIASES = {
    'luggage.LuggagePhoto': {
        'details_big': {'size': (450, 600), 'crop': False, 'upscale': False},
        'details_thumb': {'size': (43, 43), 'crop': False, 'upscale': False},
        'search_thumb': {'size': (97, 134), 'crop': False, 'upscale': False},
    }
}


# django-filebrowser config
VERSIONS_BASEDIR = '_versions'

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '../locale'),
)

# django-constance config
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'ANALYTIC_JS': ('', 'JavaScript code for anayltics'),
}


# django-compressor config
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.datauri.CssDataUriFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_DATA_URI_MAX_SIZE = 8192

COMPRESS_OUTPUT_DIR = 'cache'


# django-post-office config
EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'denisdreambits'
EMAIL_HOST_PASSWORD = 'denis123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'no-reply@luggary.com'


# recaptcha
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

SMUGGLER_FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'upload')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}




# trying to load local settings
try:
    from settings_local import *
except ImportError:
    pass


if DEBUG:
    TEMPLATE_STRING_IF_INVALID = '{error_unknown_variable_%s}'

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
