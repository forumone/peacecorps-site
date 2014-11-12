from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save


def expires(initial=None):
    """Calculate new expiration date. If no initial date is provided, use
    now"""
    if not initial:
        initial = timezone.now()
    return initial + timedelta(days=settings.PASSWORD_EXPIRE_AFTER)


class ExtraUserFields(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='extra')
    password_expires = models.DateTimeField(default=expires)


def connect_user(sender, instance, created, *args, **kwargs):
    """Make sure we always create an ExtraUserFields model when a User is
    created. Note that we cannot use the same signal trick for password
    changes, as they are not present in the list of updated fields"""
    if created:
        ExtraUserFields.objects.create(user=instance)

post_save.connect(connect_user, sender=settings.AUTH_USER_MODEL)
