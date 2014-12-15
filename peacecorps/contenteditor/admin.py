from adminsortable.admin import SortableAdminMixin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.forms import TextInput
from django.db.models import CharField

from peacecorps import models
from .forms import (
    LoggingAuthenticationForm, StrictAdminPasswordChangeForm,
    StrictUserCreationForm)


class StrictUserAdmin(UserAdmin):
    add_form = StrictUserCreationForm
    change_password_form = StrictAdminPasswordChangeForm


class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']  


class CampaignAdmin(admin.ModelAdmin):
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size':'80'})},
    }

    fieldsets = (
        ('Info', {
            'fields': ['account', 'name', ('campaigntype', 'country')]
            }),
        ('Images', {
            'fields': [('icon', 'featured_image')]
        }),
        ('Text', {
            'fields': ['tagline', 'call','slug', 'description']
        }),
        ('Projects', {
            'fields': ['featuredprojects'],
            'description': """<h4>Add projects that you want to appear on this \
                                campaign's page.</h4>"""
        }),
    )

    prepopulated_fields = {"slug": ("name",)}
    list_display = ['account', 'name']
    list_filter = ['campaigntype']
    search_fields = ['account__code', 'name', 'country__name']
    raw_id_fields = ['account', 'icon', 'featured_image', 'country']
    filter_horizontal = ['featuredprojects']


class FeaturedCampaignAdmin(admin.ModelAdmin):
    raw_id_fields = ['campaign']


class AccountInline(admin.StackedInline):
    model = models.Account


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['account', 'title', 'country', 'volunteername']
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


class FAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Country)
admin.site.register(models.FeaturedCampaign, FeaturedCampaignAdmin)
admin.site.register(models.FeaturedProjectFrontPage)
admin.site.register(models.Media)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Vignette, VignetteAdmin)
admin.site.register(models.Issue)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)
admin.site.login_form = LoggingAuthenticationForm
