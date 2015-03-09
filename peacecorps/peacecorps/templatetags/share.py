"""Provides the data for sharing over social media."""
from django.conf import settings
from django_jinja import library


@library.global_function
def share_tweet():
    return gettattr(settings, 'SHARE_TWEET', '')

def share_url(request):
    return request.build_absolute_uri()

def share_subject(request):
    return gettattr(settings, 'SHARE_SUBJECT', '')

def share_text(request):
    return gettattr(settings, 'SHARE_TEXT', '')
