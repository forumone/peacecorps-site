from django.contrib import admin

from peacecorps import models


class CampaignAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Country)
admin.site.register(models.FeaturedCampaign)
admin.site.register(models.FeaturedProjectFrontPage)
admin.site.register(models.Account)
admin.site.register(models.Media)
admin.site.register(models.Project, ProjectAdmin)
