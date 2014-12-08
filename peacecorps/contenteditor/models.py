from datetime import timedelta
import logging

from django.conf import settings
from django.contrib.admin import models as admin_models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete, post_save
import sirtrevor

from .blocks import ButtonBlock


def expires(initial=None):
    """Calculate new expiration date. If no initial date is provided, use
    now"""
    if not initial:
        initial = timezone.now()
    return initial + timedelta(days=settings.PASSWORD_EXPIRE_AFTER)


class ExtraUserFields(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='extra')
    password_expires = models.DateTimeField(default=expires)


def user_post_save(sender, instance, created, *args, **kwargs):
    """Make sure we always create an ExtraUserFields model when a User is
    created. Note that we cannot use the same signal trick for password
    changes, as they are not present in the list of updated fields. We also
    use this to log creations"""
    if created:
        ExtraUserFields.objects.create(user=instance)
        logging.getLogger("peacecorps.users").info(
            "User %s (%s) created", instance.username, instance.email)


def user_post_delete(sender, instance, *args, **kwargs):
    """Log user deletion"""
    logging.getLogger("peacecorps.users").info(
        "User %s (%s) deleted", instance.username, instance.email)


def adminlog_post_save(sender, instance, created, *args, **kwargs):
    """Django's admin already logs when edits are made. Pass that along to our
    logging system."""
    if created:
        verb_map = {admin_models.ADDITION: "added",
                    admin_models.CHANGE: "edited",
                    admin_models.DELETION: "deleted"}
        logging.getLogger("peacecorps.admin_edit").info(
            "%s (%s) %s a %s: %s (%s)", instance.user.username,
            instance.user.email, verb_map[instance.action_flag],
            instance.content_type, instance.object_repr, instance.object_id)

post_save.connect(user_post_save, sender=settings.AUTH_USER_MODEL)
post_save.connect(adminlog_post_save, sender='admin.LogEntry')
post_delete.connect(user_post_delete, sender=settings.AUTH_USER_MODEL)


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

sirtrevor.register_block(ButtonBlock)
