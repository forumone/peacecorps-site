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
        CharField: {'widget': TextInput(attrs={'size': '80'})},
    }

    fieldsets = (
        ('Info', {
            'fields': ['account', 'name', ('campaigntype', 'country'), 'icon']
            }),
        ('Text', {
            'fields': ['slug', 'description']
        }),
    )

    prepopulated_fields = {"slug": ("name",)}
    list_display = ['account', 'name']
    list_filter = ['campaigntype']
    search_fields = ['account__code', 'name', 'country__name']
    raw_id_fields = ['account', 'icon', 'country']
    # filter_horizontal = ['featuredprojects']
    exclude = ['tagline', 'call', 'featuredprojects']


class FeaturedProjectFrontPageAdmin(admin.ModelAdmin):
    list_display = ["project", "funded_status"]
    raw_id_fields = ['project']

    def funded_status(self, obj):
        if obj.project.account.funded():
            return "Funded"
        else:
            return "Not Funded"


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
    list_display = ['account', 'title', 'country',
                    'volunteername', 'funded_status']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('campaigns',)
    search_fields = ['account__code', 'volunteername', 'country__name',
                     'title']
    raw_id_fields = ['account', 'overflow',
                     'volunteerpicture', 'featured_image']
    exclude = ['media']
    readonly_fields = ['funded_status']

    def funded_status(self, obj):
        if obj.account.funded():
            return "Funded"
        else:
            return "Not Funded"

    fieldsets = (
        ('Account Info', {
            'fields': ['account', 'overflow', 'country', 'funded_status'],
            }),
        ('Volunteer Info', {
            'fields': ['volunteername',
                       'volunteerhomestate',
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
# These aren't used anywhere yet
# admin.site.register(models.Vignette, VignetteAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.unregister(User)
admin.site.register(User, StrictUserAdmin)
admin.site.login_form = LoggingAuthenticationForm
