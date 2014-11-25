import os

from .base import *


INSTALLED_APPS += ('storages',)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
ALLOWED_HOSTS = ['*']  # proxied

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

# @todo switch to memcached/elasticache
_backend = 'django.core.cache.backends.filebased.FileBasedCache'
CACHES['shortterm']['BACKEND'] = _backend
CACHES['shortterm']['LOCATION'] = '/tmp/shorttermcache/'
CACHES['midterm']['BACKEND'] = _backend
CACHES['midterm']['LOCATION'] = '/tmp/midtermcache/'

# Note that MEDIA_ROOT is not needed since we're using S3
MEDIA_URL = '//peace-corps.s3.amazonaws.com/'

GNUPG_HOME = os.environ.get('GNUPG_HOME', '')
GPG_RECIPIENTS = {
    'peacecorps.DonorInfo.xml': os.environ.get('GPG_ENCRYPT_ID', '')
}

if os.environ.get('USE_PAYGOV', ''):
    INSTALLED_APPS += ('paygov',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logstash': {
            '()': 'peacecorps.settings.logformatter.LogstashFormatter'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/webapp.log',
            'formatter': 'logstash'
        },
    },
    'loggers':  {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'peacecorps': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'paygov': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

try:
    from .local_settings import *
except ImportError:
    pass
