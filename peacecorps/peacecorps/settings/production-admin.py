from .production import *

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'tinymce',
    'contenteditor',
)
# Set these only on the machines which have admin access
LOGGED_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'peace-corps'
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


try:
    from .local_settings import *
except ImportError:
    pass
