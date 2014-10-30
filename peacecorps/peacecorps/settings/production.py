import os

from .base import *


INSTALLED_APPS += ('storages',)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # proxied
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get('PG_NAME', ''),
        "USER": os.environ.get('PG_USER', ''),
        "PASSWORD": os.environ.get('PG_PASS', ''),
        "HOST": os.environ.get('PG_HOST', ''),
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Note that MEDIA_ROOT is not needed since we're using S3
MEDIA_URL = '//peace-corps.s3.amazonaws.com/'

GNUPG_HOME = os.environ.get('GNUPG_HOME', '')
GPG_RECIPIENTS = {
    'peacecorps.fields.GPGField.xml': os.environ.get('GPG_ENCRYPT_ID', '')
}

# Add this to local settings only on the machines which pay.gov contact
# INSTALLED_APPS += ('paygov',)


try:
    from .local_settings import *
except ImportError:
    pass
