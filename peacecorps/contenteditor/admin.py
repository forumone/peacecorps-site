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


class AccountInline(admin.StackedInline):
    model = models.Account


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


class FeaturedProjectFrontPageAdmin(admin.ModelAdmin):
    raw_id_fields = ['project']


class IssueAdmin(admin.ModelAdmin):
    filter_horizontal = ['campaigns']
    search_fields = ['name']


class MediaAdmin(admin.ModelAdmin):
    fieldsets = (
    ('File', {
        'fields': ['file']
    }),
    ('Info', {
        'fields': ['title', ('mediatype', 'country'), 'caption']
        }),
    ('508 Compliance', {
        'fields': ['description', 'transcript'],
        'description': """<h4>Images must have a description.
                            Audio/video files must be transcribed.</h4>"""
    }),
)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['account', 'title', 'country', 'volunteername']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('campaigns',)
    raw_id_fields = ['account', 'overflow',
                    'volunteerpicture', 'featured_image']
    exclude = ['media']

    fieldsets = (
        ('Account Info', {
            'fields': ['account', 'overflow'],
            }),
        ('Volunteer Info', {
            'fields': ['volunteername',
                        ('volunteerhomecity', 'volunteerhomestate'),
                        'volunteerpicture'],
            'classes': ['wide']

        }),
        ('Media', {
            'fields': ['featured_image']
        }),
        ('Project Info', {
            'fields': ['title', 'tagline', 'slug',
                        'description', 'abstract', 'published']
            }),
        ('Campaigns', {
            'fields': ['campaigns']
            }),
    )


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
admin.site.register(models.FeaturedProjectFrontPage,
                    FeaturedProjectFrontPageAdmin)
admin.site.register(models.Media, MediaAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Vignette, VignetteAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)
admin.site.login_form = LoggingAuthenticationForm
