from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AdminPasswordChangeForm)
from django.utils.translation import ugettext_lazy as _

from contenteditor import models


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
