from django.db import models

from peacecorps.models import Media

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_obj(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Donate(SingletonModel):
    intro_text = models.TextField(
        max_length=255,
        help_text="Introductory Text at the top of the donations landing page.")
    about_donating = models.TextField(
        max_length=255,
        help_text="Text about how donating supports projects.")
    featured_image = models.ForeignKey(
        Media, null=True, blank=True,
        help_text="A large landscape image for the top of the page",
        related_name='donate_landing_featured_image')
    sorter_featured_image = models.ForeignKey(
        Media, null=True, blank=True,
        help_text="A large landscape image for the top of the sorter page",
        related_name='donate_sorter_featured_image')

class SitewideNotification(SingletonModel):
    enable = models.BooleanField(
        help_text="Enables the Sitewide Announcement.",
        default=False)
    header = models.CharField(
        max_length=100,
        help_text="The Header Text for the current site-wide announcement.")
    body = models.TextField(
        max_length=255,
        help_text="The body text for the site-wide announcement, viewable on first page load.")