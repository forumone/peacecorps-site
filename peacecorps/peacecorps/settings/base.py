"""
Django settings for peacecorps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DATABASES = {}
# ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',  # may be okay to remove
    'django.contrib.staticfiles',
    'restless',
    'peacecorps',
    'sirtrevor',
    'adminsortable',
    'overextends',
)


ROOT_URLCONF = 'peacecorps.urls'
WSGI_APPLICATION = 'peacecorps.wsgi.application'

TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)
# Default + request
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

INSTALLED_APPS += ('django_jinja',)
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'
JINJA2_CONSTANTS = {}
JINJA2_CONSTANTS['MINIFIED'] = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# TinyMCE configurations
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_buttons1': "bold,italic,underline,separator,bullist,separator,outdent,indent,separator,undo,redo",
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'width': '70%',
    'height': 300,
}
STATIC_ROOT = '/var/www/static/'

SIRTREVOR_DEFAULT_TYPE = 'Text'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'

USE_TZ = True
TIME_ZONE = 'UTC'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'shortterm': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'TIMEOUT': 60*5,    # 5 minutes
        'KEY_PREFIX': 'shortterm',
    },
    'midterm': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'TIMEOUT': 60*60,    # 1 hour
        'KEY_PREFIX': 'midterm',
    }
}

# APP_SPECIFIC_VALUES

# Not secret information -- it's in donation form
PAY_GOV_AGENCY_ID = '1247'
PAY_GOV_APP_NAME = 'DONORPAGES2'
PAY_GOV_FORM_ID = 'DONORPAGES2'

# The URL for the pay.gov payment service.
PAY_GOV_OCI_URL = os.environ.get('PAY_GOV_OCI_URL', 'https://example.com/')

# DonorInfo objects expire after a set period of time
DONOR_EXPIRE_AFTER = 30      # minutes

# Where to cut project "abstract"s
ABSTRACT_LENGTH = 256

# GPG info for encrypted fields
GNUPG_HOME = ''     # Directory containing keys. If empty, GPG will not be used
GPG_RECIPIENTS = {
    'peacecorps.DonorInfo.xml': '00000000'
}

# Password expire after a set number of days
PASSWORD_EXPIRE_AFTER = 60   # days
# Admin paths which can be accessible even when the password has expired
PASSWORD_EXPIRATION_WHITELIST = [
    '/admin/login/',
    '/admin/logout/',
    '/admin/jsi18n/'
]

AUTHENTICATION_BACKENDS = ('contenteditor.backends.EditorBackend',)
DEFAULT_FILE_STORAGE = 'contenteditor.backends.LoggingStorage'
# The logging storage (above) must have a backend. Default to Django's default
LOGGED_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Non-Sir Trevor Image Processing:
RESIZED_IMAGE_UPLOAD_PATH = "attachments/"

# Sir Trevor image storage and processing:
SIRTREVOR_UPLOAD_PATH = "attachments/"

# Sir Trevor Blocks:
SIRTREVOR_BLOCK_TYPES = ['Text', 'Image508']

# Used when generating tweets/emails
SHARE_SUBJECT = "Peacecorps Donation"
SHARE_TEMPLATE = "I just donated to a great cause! %s"

# Used to color issue icons
SVG_COLORS = {
    'white': '#FFF',
    'grey': '#67655D'
}
