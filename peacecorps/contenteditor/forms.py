import logging

from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm)
from django.utils.translation import ugettext_lazy as _

from contenteditor import models


class LoggingAuthenticationForm(AdminAuthenticationForm):
    """Override login form to log attempts"""
    def clean(self):
        logger = logging.getLogger("peacecorps.login")
        try:
            cleaned = super(LoggingAuthenticationForm, self).clean()
            logger.info("%s successfully logged in",
                        self.cleaned_data['username'])
            return cleaned
        except forms.ValidationError:
            logger.warn("Failed login attempt for %s",
                        self.cleaned_data.get('username'))
            raise


class StrictUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput, help_text=_("""
            Enter a password. Requirements include: at least 20 characters,
            at least one uppercase letter, at least one lowercase letter, at
            least one number, and at least one special character.
            """))

    def clean_password1(self):
        """Adds to the default password validation routine in order to enforce
        stronger passwords"""
        password = self.cleaned_data['password1']
        errors = models.password_errors(password)

        # If password_validator returns errors, raise an error, else proceed.
        if errors:
            raise forms.ValidationError('\n'.join(errors))
        else:
            return password


class StrictAdminPasswordChangeForm(AdminPasswordChangeForm):
    """Password form for editing a user"""
    password1 = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput, help_text=_("""
            Enter a password. Requirements include: at least 20 characters,
            at least one uppercase letter, at least one lowercase letter, at
            least one number, and at least one special character.
            """))

    def clean_password1(self):
        """Adds to the default password validation routine in order to enforce
        stronger passwords"""
        password = self.cleaned_data['password1']
        errors = models.password_errors(password)
        # Also check that this is a new password
        if self.user.check_password(self.cleaned_data['password1']):
            errors.append("Must not reuse a password")

        # If password_validator returns errors, raise an error, else proceed.
        if errors:
            raise forms.ValidationError('\n'.join(errors))
        else:
            return password

    def save(self):
        user = super(StrictAdminPasswordChangeForm, self).save()
        user.extra.password_expires = models.expires()
        user.extra.save()
        return user


class StrictPasswordChangeForm(PasswordChangeForm):
    """Password form residing at /admin/password_change"""
    new_password1 = forms.CharField(
        label=_("New password"), widget=forms.PasswordInput, help_text=_("""
            Enter a password. Requirements include: at least 20 characters,
            at least one uppercase letter, at least one lowercase letter, at
            least one number, and at least one special character.
            """))

    def clean_new_password1(self):
        """Adds to the default password validation routine in order to enforce
        stronger passwords"""
        password = self.cleaned_data['new_password1']
        errors = models.password_errors(password)
        # Also check that this is a new password
        if self.user.check_password(self.cleaned_data['new_password1']):
            errors.append("Must not reuse a password")

        # If password_validator returns errors, raise an error, else proceed.
        if errors:
            raise forms.ValidationError('\n'.join(errors))
        else:
            return password

    def save(self):
        user = super(StrictPasswordChangeForm, self).save()
        user.extra.password_expires = models.expires()
        user.extra.save()
        return user
