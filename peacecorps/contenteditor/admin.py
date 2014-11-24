from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import (
    LoggingAuthenticationForm, StrictAdminPasswordChangeForm,
    StrictUserCreationForm)


class StrictUserAdmin(UserAdmin):
    add_form = StrictUserCreationForm
    change_password_form = StrictAdminPasswordChangeForm


admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)
admin.site.login_form = LoggingAuthenticationForm
