"""Provides the data for sharing over social media."""
from django.conf import settings
from django_jinja import library


@library.global_function
def share_tweet():
    return getattr(settings, 'SHARE_TWEET', '')

@library.global_function
def share_url(request, override=None):
    if override is None:
        return request.build_absolute_uri()
    return override

@library.global_function
def share_subject():
    return getattr(settings, 'SHARE_SUBJECT', '')

@library.global_function
def share_text():
    return getattr(settings, 'SHARE_TEMPLATE', '')
