# coding: utf-8

from os.path import dirname, join, realpath
import sys

_current_dir = dirname(realpath(__file__))


###############################################################################
# Basic settings
###############################################################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('voy', 'voyageur.pl@gmail.com'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = []
SECRET_KEY = 'u=c2brcszbq7r45^94)xdi(lz=d^%-yoi(38xwq5k0u*8wmb3v'
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'


###############################################################################
# Databases settings
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stwa',
        'USER': 'stwa',
        'PASSWORD': 'stwa',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

# switch to sqlite for tests
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

###############################################################################
# Localization settings
###############################################################################

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_INPUT_FORMATS = (
    '%H:%M:%S',
    '%H:%M',
    '%H.%M.%S',
    '%H.%M',
    '%H,%M,%S',
    '%H,%M',
)

###############################################################################
# Staticfiles/media/templates settings
###############################################################################

MEDIA_ROOT = join(_current_dir, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = join(_current_dir, 'public_html')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    # core
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # third party
    'djangobower.finders.BowerFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
)


###############################################################################
# Middleware, installed apps, processors
###############################################################################

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # core
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    #internal
    "app.shared.context_processors.settings_values",
)

INSTALLED_APPS = filter(None, [
    # core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # third-party
    'debug_toolbar' if DEBUG else None,
    'django_coverage',
    'djangobower',
    'gravatar',
    'south',
    'django_nose',  # https://github.com/jbalogh/django-nose#using-with-south
    'widget_tweaks',

    # internal
    'app.accounts',
    'app.home',
    'app.shared',
    'app.health',
    'app.activities',
    'app.routes',
    'app.workouts',
])

BOWER_INSTALLED_APPS = (
    'fullcalendar',
)


###############################################################################
# Third party apps settings
###############################################################################

# Tests
SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


# Gravatar
# http://github.com/v0y/django-gravatar
GRAVATAR_CHANGE_URL = 'http://gravatar.com/emails/'
GRAVATAR_DEFAULT_IMAGE = 'monsterid'
GRAVATAR_DEFAULT_SIZE = 210
GRAVATAR_IMG_CLASS = 'thumbnail'


# debug_toolbar
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1', ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False
    }


# Django Bower
BOWER_COMPONENTS_ROOT = join(_current_dir, 'components')


###############################################################################
# Core/internal apps settings
###############################################################################

# Accounts
REDIRECT_AFTER_LOGIN = '/'
REDIRECT_AFTER_LOGOUT = '/'
ACCOUNT_ACTIVATION_DAYS = 7
PASSWORD_RESET_TIMEOUT_DAYS = 3
EMAIL_CHANGE_TIMEOUT_DAYS = 3
LOGIN_URL = '/accounts/login'


###############################################################################
# Email settings
###############################################################################

# email configuration
DEFAULT_FROM_EMAIL = 'no-reply@example.com'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # TODO: konfiguracja SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = ''
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False


###############################################################################
# keys
###############################################################################

GOOGLE_BROWSER_KEY = 'AIzaSyA5B9zYYg9j-FwwHVggUuATjF5gtnWknDk'
