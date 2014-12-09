from datetime import timedelta
import json

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.template.loader import render_to_string as django_render
from django.utils import timezone
from django.utils.text import slugify
from localflavor.us.models import USPostalCodeField
from sirtrevor.fields import SirTrevorField

from peacecorps.fields import GPGField, BraveSirTrevorField


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
        return '%s' % (self.code)

    def total(self):
        donations = self.donations.aggregate(Sum('amount'))
        if donations['amount__sum']:
            return self.current + donations['amount__sum']
        else:
            return self.current

    def percent_funded(self):
        if self.goal:
            return percentfunded(self.total() + self.community_contribution,
                                 self.goal + self.community_contribution)
        else:
            return 0

    def percent_community_funded(self):
        return percentfunded(self.community_contribution,
                             self.goal + self.community_contribution)

    def funded(self):
        if self.goal and self.total() >= self.goal:
            return True
        else:
            return False

    def remaining(self):
        """This will be expanded later, and may involve more complicated
        calculations. As such, we don't want it to be a property"""
        return self.goal - self.total()


# @todo: this description isn't really accurate anymore. Probably worth
# renaming
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
    account = models.ForeignKey(
        'Account', to_field='code', unique=True, blank=True, null=True)
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
    description = BraveSirTrevorField(help_text="the full description.")
    featuredprojects = models.ManyToManyField('Project', blank=True, null=True)
    country = models.ForeignKey(
        'Country', related_name="campaign", blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Campaign, self).save(*args, **kwargs)


class SectorMapping(models.Model):
    """When importing data from the accounting software, a 'sector' field
    indicates how individual projects should be categorized. The text used in
    this field does not directly match anything we store, however, so we use a
    mapping object, which is populated on data import."""
    accounting_name = models.CharField(max_length=50, primary_key=True)
    campaign = models.ForeignKey(Campaign)


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
    project = models.ForeignKey('Project',
                                limit_choices_to={'published': True})

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
        briefly describe what it depicts. Do not use html formatting.")
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
        max_length=240, help_text="a short description for subheadings.",
        blank=True, null=True)
    slug = models.SlugField(max_length=100, help_text="for the project url.")
    description = BraveSirTrevorField(help_text="the full description.")
    country = models.ForeignKey('Country', related_name="projects")
    campaigns = models.ManyToManyField(
        'Campaign',
        help_text="Campaigns to which this project belongs",
        blank=True, null=True)
    featured_image = models.ForeignKey(
        'Media', null=True, blank=True,
        help_text="A large landscape image for use in banners, headers, etc")
    media = models.ManyToManyField(
        'Media', related_name="projects", blank=True, null=True)
    account = models.ForeignKey('Account', to_field='code', unique=True)
    overflow = models.ForeignKey(
        'Account', related_name="overflow", blank=True, null=True)
    volunteername = models.CharField(max_length=100)
    volunteerpicture = models.ForeignKey(
        'Media', related_name="volunteer", blank=True, null=True)
    volunteerhomestate = USPostalCodeField(blank=True, null=True)
    volunteerhomecity = models.CharField(max_length=120, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)

    published = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return self.title

    def abstract_html(self):
        """If an explicit abstract is present, return it. Otherwise, return
        the formatted first paragraph of the description"""
        if self.abstract:
            return self.abstract
        elif self.description:
            for block in json.loads(self.description)['data']:
                if block.get('type') == 'text':
                    data = block['data']
                    # Naive string shortener
                    if len(data['text']) > settings.ABSTRACT_LENGTH:
                        trimmed = data['text'][:settings.ABSTRACT_LENGTH]
                        trimmed = trimmed[:trimmed.rindex(' ')]
                        data = {'text': trimmed + '...'}
                    return django_render('sirtrevor/blocks/text.html', data)
        return ''

    def save(self, *args, **kwargs):
        """Set slug, but make sure it is distinct"""
        if not self.slug:
            self.slug = slugify(self.title)
            existing = Project.objects.filter(
                # has some false positives, but almost no false negatives
                slug__startswith=self.slug).order_by('-pk').first()
            if existing:
                self.slug = self.slug + str(existing.pk)
        super(Project, self).save(*args, **kwargs)

    def issue(self, check_cache=True):
        """Find the "first" issue that this project is associated with, if
        any"""
        if not check_cache or not hasattr(self, '_issue'):
            issue_data = self.campaigns.values_list(
                'issue__pk', 'issue__name').filter(
                issue__pk__isnull=False).order_by('issue__name').first()
            if issue_data:
                self._issue = Issue.objects.get(pk=issue_data[0])
            else:
                self._issue = None
        return self._issue


class Issue(models.Model):
    """A categorization scheme. This could eventually house relationships with
    individual projects, but for now, just point to sector funds"""
    name = models.CharField(max_length=100)
    icon = models.FileField()   # No need for any of the 'Media' fields
    campaigns = models.ManyToManyField(
        Campaign, limit_choices_to={'campaigntype': Campaign.SECTOR})

    def __str__(self):
        return self.name

    def projects(self):
        """Jump through the campaigns connection to get to a set of projects"""
        campaigns = self.campaigns.all()
        return Project.published_objects.filter(campaigns__in=campaigns)


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


class Vignette(models.Model):
    """Chunk of content with a unique identifier. This allows otherwise static
    content to be edited by admins"""
    slug = models.CharField(max_length=50, primary_key=True)
    location = models.TextField()
    instructions = models.TextField()
    content = SirTrevorField()

    def __str__(self):
        return self.slug

    @staticmethod
    def for_slug(slug):
        """Return the requested vignette if it exists, and one with a warning
        if not"""
        vig = Vignette.objects.filter(slug=slug).first()
        if not vig:
            vig = Vignette(slug=slug, content=json.dumps({'data': [
                {'type': 'text', 'data': {
                    'text': 'Missing Vignette `' + slug + '`'}}]}))
        return vig
