from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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


class Editor(User):
    """Content editors (synonymous with user in our application) has specific
    requirements for setting user passwords."""
    class Meta:
        proxy = True

    def set_password(self, raw_password):
        """We add special password validation checks here"""
        errors = password_errors(raw_password)
        if errors:
            raise ValidationError(" ".join(errors))
        return super(Editor, self).set_password(raw_password)


def password_errors(password):
    """Validates a given string against required password params. This is
    required in order to maintain FISMA compliance."""
    # Set up an errors array to capture things we find
    errors = []
    password = password or ""   # account for Nones

    # Defines special characters we allow
    # TODO: I guess this could be a regex instead, I just typed all the
    # chars on my keyboard :)
    valid_special_chars = set('~`!@#$%^&*()-_=+[{]}\|;:'",<.>/?/*-.+")
    if not password:
        errors.append('Password cannot be blank.')
    if not any(x.isupper() for x in password):
        errors.append('Password needs at least one uppercase letter.')
    if not any(x.islower() for x in password):
        errors.append('Password needs at least one lowercase letter.')
    if not any(x.isdigit() for x in password):
        errors.append('Password needs at least one number.')
    if not any((x in valid_special_chars) for x in password):
        errors.append('Password needs a special character.')
    if not len(password) >= 20:
        errors.append('Password must be at least 20 characters in length.')

    return errors
