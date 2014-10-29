from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (UserCreationForm,
    AdminPasswordChangeForm)
from django.contrib.auth.models import User

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _


from peacecorps import models

# Password length requirements
def password_validator(password):
    """Validates a given string against required password params. This is
    required in order to maintain FISMA compliance."""
    # Set up an errors array to capture things we find
    errors = []

    # Defines special characters we allow
    # TODO: I guess this could be a regex instead, I just typed all the chars
    # on my keyboard :)
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


class StrictUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput, help_text=_("""
            Enter a password. Requirements include: at least 20 characters,
            at least one uppercase letter, at least one lowercase letter, at
            least one number, and at least one special character.
            """))

    def clean_password1(self):
        """Adds to the default password validation routine in order to enforce 
        stronger passwords"""
        password = self.cleaned_data['password1']
        errors = password_validator(password)

        # If password_validator returns errors, raise an error, else proceed.
        if errors:
            raise forms.ValidationError('\n'.join(errors))
        else:
            return password

class StrictAdminPasswordChangeForm(AdminPasswordChangeForm):
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput, help_text=_("""
            Enter a password. Requirements include: at least 20 characters,
            at least one uppercase letter, at least one lowercase letter, at
            least one number, and at least one special character.
            """))
    
    def clean_password1(self):
        """Adds to the default password validation routine in order to enforce 
        stronger passwords"""
        password = self.cleaned_data['password1']
        errors = password_validator(password)

        # If password_validator returns errors, raise an error, else proceed.
        if errors:
            raise forms.ValidationError('\n'.join(errors))
        else:
            return password

class StrictUserAdmin(UserAdmin):
    add_form = StrictUserCreationForm
    change_password_form = StrictAdminPasswordChangeForm


class IssueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class FundDisplayAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class MemorialFundAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CountryFundAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(models.Country)
admin.site.register(models.CountryFund, CountryFundAdmin)
admin.site.register(models.FeaturedIssue)
admin.site.register(models.FeaturedCampaign)
admin.site.register(models.FeaturedProjectFrontPage)
admin.site.register(models.Fund)
admin.site.register(models.FundDisplay, FundDisplayAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.Media)
admin.site.register(models.MemorialFund, MemorialFundAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)

