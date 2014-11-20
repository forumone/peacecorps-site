from django.contrib import admin

from peacecorps import models


class CampaignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class AccountInline(admin.StackedInline):
    model = models.Account


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'volunteername', 'account']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('campaigns',)


admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Country)
admin.site.register(models.FeaturedCampaign)
admin.site.register(models.FeaturedProjectFrontPage)
admin.site.register(models.Account)
admin.site.register(models.Media)
admin.site.register(models.Project, ProjectAdmin)
