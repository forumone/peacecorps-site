from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log'
        },
    },
    'loggers':  {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MEDIA_ROOT = './media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/static/'

try:
    from .local_settings import *
except ImportError:
    pass
