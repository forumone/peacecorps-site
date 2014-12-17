"""Wrap a path in the default media root. This is only needed for photos
managed outside of the CMS"""
from django.conf import settings
from django_jinja import library


@library.global_function
def media(url):
    return getattr(settings, 'MEDIA_URL', '') + url
