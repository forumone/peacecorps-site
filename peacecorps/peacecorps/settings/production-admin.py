from .production import *

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'tinymce',
    'storages',
    'contenteditor',
)
# Only media uploads are logged
LOGGED_FILE_STORAGE = 'contenteditor.backends.MediaS3Storage'
# We are not using this setting in favor of the two below it
# AWS_STORAGE_BUCKET_NAME = 'peace-corps'
AWS_MEDIA_BUCKET_NAME = 'pc-media-dev'
AWS_STATIC_BUCKET_NAME = 'pc-theme-dev'
STATICFILES_STORAGE = 'contenteditor.backends.StaticS3Storage'

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
