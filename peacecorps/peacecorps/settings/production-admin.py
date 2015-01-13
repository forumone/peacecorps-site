from .production import *

INSTALLED_APPS += (
    'contenteditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'tinymce',
    'storages',
)
# Only media uploads are logged
LOGGED_FILE_STORAGE = 'contenteditor.backends.MediaS3Storage'
# We are not using this setting in favor of the two below it
# AWS_STORAGE_BUCKET_NAME = 'peace-corps'
AWS_MEDIA_BUCKET_NAME = 'pc-media-dev'
AWS_STATIC_BUCKET_NAME = 'pc-theme-dev'

STATICFILES_STORAGE = 'contenteditor.backends.StaticS3Storage'

AWS_QUERYSTRING_AUTH = False

# Turn off caching for the admin app
CACHES['shortterm']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['midterm']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Include Sir Trevor urls:
SIRTREVOR = True

try:
    from .local_settings import *
except ImportError:
    pass
