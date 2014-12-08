from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from peacecorps import models
from .forms import (
    LoggingAuthenticationForm, StrictAdminPasswordChangeForm,
    StrictUserCreationForm)


class StrictUserAdmin(UserAdmin):
    add_form = StrictUserCreationForm
    change_password_form = StrictAdminPasswordChangeForm


class CampaignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class AccountInline(admin.StackedInline):
    model = models.Account


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'volunteername', 'account']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('campaigns',)


class VignetteAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('slug', 'location')
    fields = ('location', 'instructions', 'content')
    readonly_fields = ('location', 'instructions')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Country)
admin.site.register(models.FeaturedCampaign)
admin.site.register(models.FeaturedProjectFrontPage)
admin.site.register(models.Account)
admin.site.register(models.Media)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Vignette, VignetteAdmin)
admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)
admin.site.login_form = LoggingAuthenticationForm
