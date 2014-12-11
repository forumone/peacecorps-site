from django.conf import settings
from django.views.decorators.cache import cache_page


def midterm_cache(*args, **kwargs):
    return cache_page(settings.CACHES['midterm']['TIMEOUT'],
                      cache='midterm')(*args, **kwargs)


def shortterm_cache(*args, **kwargs):
    return cache_page(settings.CACHES['shortterm']['TIMEOUT'],
                      cache='shortterm')(*args, **kwargs)
