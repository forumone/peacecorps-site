from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .form import (
    StrictAdminPasswordChangeForm, StrictUserCreationForm)
from .models import Editor


class StrictUserAdmin(UserAdmin):
    add_form = StrictUserCreationForm
    change_password_form = StrictAdminPasswordChangeForm

    def __init__(self, *args, **kwargs):
        super(StrictUserAdmin, self).__init__(*args, **kwargs)
        self.model = Editor


admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)
