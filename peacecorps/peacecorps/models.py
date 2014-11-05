from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from localflavor.us.models import USPostalCodeField
from tinymce import models as tinymce_models

from peacecorps.fields import GPGField


def percentfunded(current, goal):
    try:
        return round((current/goal)*100, 2)
    except ZeroDivisionError:
        return 0


def humanize_amount(amount_cents):
    """ Return a string that presents the donation amount in a humanized
    format. """

    amount_dollars = amount_cents/100.0
    return "${:,.2f}".format(amount_dollars)


class Account(models.Model):
    COUNTRY = 'coun'
    MEMORIAL = 'mem'
    OTHER = 'oth'
    PROJECT = 'proj'
    SECTOR = 'sec'
    CATEGORY_CHOICES = (
        (COUNTRY, 'Country'),
        (SECTOR, 'Sector'),
        (MEMORIAL, 'Memorial'),
        (OTHER, 'Other'),
        (PROJECT, 'Project'),
    )

    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=25, unique=True)
    current = models.IntegerField(default=0)
    goal = models.IntegerField(blank=True, null=True)
    community_contribution = models.IntegerField(blank=True, null=True)
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return '%s' % (self.name)

    def total(self):
        donations = self.donations.aggregate(Sum('amount'))
        if donations['amount__sum']:
            return self.current + donations['amount__sum']
        else:
            return self.current

    def percent_funded(self):
        return percentfunded(self.total(), self.goal)

    def funded(self):
        if self.goal and self.total() >= self.goal:
            return True
        else:
            return False

    def remaining(self):
        """This will be expanded later, and may involve more complicated
        calculations. As such, we don't want it to be a property"""
        return self.goal - self.total()


class Campaign(models.Model):
    """
    A campaign is any fundraising effort. Campaigns can collect donations
    to a separate account that can be distributed to projects (sector, country,
    special, and memorial funds, the general fund), or they can exist simply to
    group related projects to highlight them to interested parties.
    """
    COUNTRY = 'coun'
    GENERAL = 'gen'
    MEMORIAL = 'mem'
    OTHER = 'oth'
    SECTOR = 'sec'
    TAG = 'tag'  # a group of campaigns that doesn't have an account attached.
    CAMPAIGNTYPE_CHOICES = (
        (COUNTRY, 'Country'),
        (GENERAL, 'General'),
        (SECTOR, 'Sector'),
        (MEMORIAL, 'Memorial'),
        (OTHER, 'Other'),
        (TAG, 'Tag')
    )

    name = models.CharField(max_length=120)
    account = models.ForeignKey('Account', unique=True, blank=True, null=True)
    campaigntype = models.CharField(
        max_length=10, choices=CAMPAIGNTYPE_CHOICES)
    icon = models.ForeignKey(
        'Media',
        related_name="campaign-icon",
        help_text="A small icon to represent this on the landing page.",
        blank=True, null=True)
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc",
        blank=True, null=True)
    tagline = models.CharField(
        max_length=140,
        help_text="a short phrase for banners (140 characters)",
        blank=True, null=True)
    call = models.CharField(
        max_length=50, help_text="call to action for buttons (50 characters)",
        blank=True, null=True)
    slug = models.SlugField(
        help_text="used for the campaign page url.",
        max_length=100, unique=True)
    description = tinymce_models.HTMLField()
    featuredprojects = models.ManyToManyField('Project', blank=True, null=True)

    def __str__(self):
        return self.name

    # TODO: slugify in admin, override save to preserve unique on general?


class Country(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)


class FeaturedCampaign(models.Model):
    campaign = models.ForeignKey('Campaign')

    # Much like the Highlander, there can be only one.
    def save(self):
        for cam in FeaturedCampaign.objects.all():
            cam.delete()
        self.id = 1
        super(FeaturedCampaign, self).save()

    def __str__(self):
        return '%s (Featured)' % (self.campaign.name)


class FeaturedProjectFrontPage(models.Model):
    project = models.ForeignKey('Project')

    def __str__(self):
        return '%s (Featured)' % (self.project.title)


class Media(models.Model):
    IMAGE = "IMG"
    VIDEO = "VID"
    AUDIO = "AUD"
    OTHER = "OTH"
    MEDIATYPE_CHOICES = (
        (IMAGE, "Image"),
        (VIDEO, "Video"),
        (AUDIO, "Audio"),
        (OTHER, "Other"),
    )

    title = models.CharField(max_length=100)
    file = models.FileField()  # TODO: Configure
    mediatype = models.CharField(
        max_length=3, choices=MEDIATYPE_CHOICES, default=IMAGE)
    caption = models.TextField(blank=True, null=True)
    country = models.ForeignKey('Country', blank=True, null=True)
    description = models.TextField(
        help_text="Provide an image description for users with screenreaders. \
        If the image has text, transcribe the text here. If it's a photo, \
        briefly describe the scene. For design elements like icons, bullets, \
        etc, leave this field blank.")
    transcript = models.TextField(
        help_text="Please transcribe audio for users with disabilities.",
        blank=True, null=True)

    def __str__(self):
        return '%s' % (self.title)

    @property
    def url(self):
        return self.file.url


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(
            published=True)


class Project(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(
        max_length=240, help_text="a short description for subheadings.")
    slug = models.SlugField(max_length=100, help_text="for the project url.")
    description = tinymce_models.HTMLField(help_text="the full description.")
    country = models.ForeignKey('Country', related_name="projects")
    campaigns = models.ManyToManyField(
        'Campaign',
        help_text="Campaigns to which this project belongs",
        blank=True, null=True)
    featured_image = models.ForeignKey(
        'Media', null=True,
        help_text="A large landscape image for use in banners, headers, etc")
    media = models.ManyToManyField(
        'Media', related_name="projects", blank=True, null=True)
    account = models.ForeignKey('Account', unique=True)
    overflow = models.ForeignKey(
        'Account', related_name="overflow", blank=True, null=True)
    volunteername = models.CharField(max_length=100)
    volunteerpicture = models.ForeignKey(
        'Media', related_name="volunteer", blank=True, null=True)
    volunteerhomestate = USPostalCodeField(blank=True, null=True)
    volunteerhomecity = models.CharField(max_length=120, blank=True, null=True)

    published = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return self.title


def default_expire_time():
    return timezone.now() + timedelta(minutes=settings.DONOR_EXPIRE_AFTER)


class DonorInfo(models.Model):
    """Represents a blob of donor information which will be requested by
    pay.gov. We need to limit accessibility as it contains PII"""
    agency_tracking_id = models.CharField(max_length=21, primary_key=True)
    account = models.ForeignKey(Account, related_name='donorinfos')
    xml = GPGField()
    expires_at = models.DateTimeField(default=default_expire_time)


class Donation(models.Model):
    """Log donation amounts as received from pay.gov"""
    account = models.ForeignKey(Account, related_name='donations')
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
