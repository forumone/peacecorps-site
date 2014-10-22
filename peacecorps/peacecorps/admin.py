from django.contrib import admin

from peacecorps import models


class IssueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CountryFundAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(models.Country)
admin.site.register(models.CountryFund, CountryFundAdmin)
admin.site.register(models.FeaturedIssue)
admin.site.register(models.FeaturedProjectFrontPage)
admin.site.register(models.Fund)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.Media)
admin.site.register(models.Project, ProjectAdmin)

