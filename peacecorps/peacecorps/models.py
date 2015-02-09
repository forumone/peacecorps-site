from datetime import timedelta
import json
import tempfile
import os

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.template.loader import render_to_string as django_render
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.storage import default_storage
from localflavor.us.models import USPostalCodeField
from localflavor.us.us_states import USPS_CHOICES
from sirtrevor.fields import SirTrevorField
from PIL import Image

from peacecorps.fields import GPGField, BraveSirTrevorField
from peacecorps.util import svg


NAME_LENGTH = 120   # Consistent length for project/account/fund names
ABBR_TO_STATE = dict(USPS_CHOICES)


def imagesave(description):
    """Saves images from Sir Trevor fields to the media model."""
    if not description:
        # if description is empty for any reason, it has no images.
        return False

    description = json.loads(description)

    for block in description['data']:
        if block['type'] == 'image508':
            imagepath = block['data']['file']['path']

            desc = block['data']['image_description']

            thisimage = Media.objects.filter(file=imagepath).first()
            if thisimage is None:
                thisimage = Media(file=imagepath)
            thisimage.title = block['data']['image_title']
            thisimage.mediatype = Media.IMAGE
            thisimage.description = desc

            thisimage.save()

    return True


class AbstractHTMLMixin(object):
    """Adds the abstract_html method. Assumes the object has an abstract and
    description field, where the description field is sir-trevor json"""
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


class AccountManager(models.Manager):
    """We more or less always want to aggregate the dynamic number of
    donations, so add it to the default query set"""
    def get_queryset(self):
        return super(AccountManager, self).get_queryset().annotate(
            dynamic_total=Sum('donations__amount'))


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

    name = models.CharField(max_length=NAME_LENGTH, unique=True)
    code = models.CharField(max_length=25, primary_key=True)
    current = models.IntegerField(
        default=0,
        help_text="Amount from donations (excluding real-time), in cents")
    goal = models.IntegerField(
        blank=True, null=True,
        help_text="Donations goal (excluding community contribution)")
    # @todo does it make sense for this to default zero?
    community_contribution = models.IntegerField(blank=True, null=True)
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES)

    objects = AccountManager()

    def __str__(self):
        return '%s' % (self.code)

    def total_donated(self):
        """Total amount raised via donations (including real-time). Does not
        include community contributions"""
        if not hasattr(self, 'dynamic_total'):
            agg = self.donations.aggregate(Sum('amount'))
            self.dynamic_total = agg['amount__sum']
        return self.current + (self.dynamic_total or 0)

    def total_raised(self):
        """Total amount raised, including donations and community
        contributions"""
        return self.total_donated() + (self.community_contribution or 0)

    def total_cost(self):
        """Total cost of whatever we are raising funds for. This includes the
        donations goal and the community contribution"""
        if self.goal:
            return self.goal + (self.community_contribution or 0)
        else:
            return 0

    def percent_raised(self):
        """What percent of the total cost has been raised through donations
        and community contributions?"""
        total_cost = self.total_cost()
        if total_cost:
            return round(self.total_raised() * 100 / total_cost, 2)
        else:
            return 0

    def percent_community(self):
        """What percent of the total cost was community contributions?"""
        total_cost = self.total_cost()
        if total_cost:
            return round(self.community_contribution * 100 / total_cost, 2)
        else:
            return 0

    def funded(self):
        if self.goal and self.total_donated() >= self.goal:
            return True
        else:
            return False

    def remaining(self):
        """This will be expanded later, and may involve more complicated
        calculations. As such, we don't want it to be a property"""
        if self.goal:
            return self.goal - self.total_donated()
        else:
            return 0

    def project_or_fund(self):
        """Given an account, we may need to get back to the project or
        campaign/fund associated"""
        if self.category == Account.PROJECT:
            return self.project_set.first()
        else:
            return self.campaign_set.first()


# @todo: this description isn't really accurate anymore. Probably worth
# renaming
class Campaign(models.Model, AbstractHTMLMixin):
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

    name = models.CharField(max_length=NAME_LENGTH)
    account = models.ForeignKey('Account', unique=True)
    campaigntype = models.CharField(
        max_length=10, choices=CAMPAIGNTYPE_CHOICES)
    icon = models.ForeignKey(
        'Media',
        # related_name="campaign-icon",
        help_text="A small photo to represent this campaign on the site.",
        blank=True, null=True)
    tagline = models.CharField(
        max_length=140,
        help_text="a short phrase for banners (140 characters)",
        blank=True, null=True)
    call = models.CharField(
        max_length=50, help_text="call to action for buttons (50 characters)",
        blank=True, null=True)
    slug = models.SlugField(
        help_text="Auto-generated. Used for the campaign page url.",
        max_length=NAME_LENGTH, unique=True)
    description = BraveSirTrevorField(help_text="the full description.")
    featuredprojects = models.ManyToManyField('Project', blank=True, null=True)
    country = models.ForeignKey(
        'Country', related_name="campaign", blank=True, null=True, unique=True)
    abstract = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.account_id, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        """Save images to the Media model"""
        imagesave(self.description)

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
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)


class FeaturedCampaign(models.Model):
    campaign = models.ForeignKey('Campaign', to_field='account')

    # Much like the Highlander, there can be only one.
    def save(self):
        for cam in FeaturedCampaign.objects.all():
            cam.delete()
        self.id = 1
        super(FeaturedCampaign, self).save()

    def __str__(self):
        return '%s: %s (Featured)' % (self.campaign.account_id,
                                      self.campaign.name)


class FeaturedProjectFrontPage(models.Model):
    project = models.ForeignKey('Project', to_field='account',
                                limit_choices_to={'published': True})

    def __str__(self):
        return '%s: %s (Featured)' % (self.project.account_id,
                                      self.project.title)


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

    title = models.CharField(max_length=NAME_LENGTH)
    file = models.FileField()
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

    def save(self, *args, **kwargs):
        if self.mediatype == Media.IMAGE:
            SIZES = (('lg', 1200, 1200), ('md', 900, 900), ('sm', 500, 500),
                     ('thm', 300, 300))

            img = Image.open(self.file.file)
            filename, filetype = self.file.name.rsplit('.', 1)

            for ext, width, height in SIZES:
                thisfile = filename + '-' + ext + '.' + filetype
                if not os.path.exists(os.path.join(
                        settings.MEDIA_ROOT,
                        settings.RESIZED_IMAGE_UPLOAD_PATH, thisfile)):
                    with tempfile.TemporaryFile() as buffer_file:
                        img.thumbnail((width, height), Image.ANTIALIAS)
                        path = os.path.join(
                            settings.RESIZED_IMAGE_UPLOAD_PATH, thisfile)
                        img.save(buffer_file, img.format.lower())
                        default_storage.save(path, buffer_file)
            self.file.file.seek(0)
        super(Media, self).save(*args, **kwargs)

    @property
    def url(self):
        return self.file.url


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(
            published=True)


class Project(models.Model, AbstractHTMLMixin):
    title = models.CharField(max_length=NAME_LENGTH)
    tagline = models.CharField(
        max_length=240, help_text="a short description for subheadings.",
        blank=True, null=True)
    slug = models.SlugField(max_length=NAME_LENGTH,
                            help_text="for the project url.")
    description = BraveSirTrevorField(help_text="the full description.")
    country = models.ForeignKey('Country', related_name="projects")
    campaigns = models.ManyToManyField(
        'Campaign',
        help_text="The campaigns to which this project belongs.",
        blank=True, null=True)
    featured_image = models.ForeignKey(
        'Media', null=True, blank=True,
        help_text="A large landscape image for use in banners, headers, etc")
    media = models.ManyToManyField(
        'Media', related_name="projects", blank=True, null=True)
    account = models.ForeignKey('Account', unique=True)
    overflow = models.ForeignKey(
        'Account', blank=True, null=True, related_name='overflow',
        help_text="""Select another fund to which users will be directed to
                    donate if the project is already funded.""")
    volunteername = models.CharField(max_length=NAME_LENGTH)
    volunteerpicture = models.ForeignKey(
        'Media', related_name="volunteer", blank=True, null=True)
    volunteerhomestate = USPostalCodeField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)

    published = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Set slug, but make sure it is distinct"""
        if not self.slug:
            self.slug = slugify(self.title)
            existing = Project.objects.filter(
                # has some false positives, but almost no false negatives
                slug__startswith=self.slug).order_by('-pk').first()
            if existing:
                self.slug = self.slug + str(existing.pk)

        """Save images to the Media model"""
        imagesave(self.description)

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

    def volunteer_statename(self):
        """Look up the volunteer's state name by abbreviation. If it
        can't be found, just use the abbreviation"""
        return ABBR_TO_STATE.get(self.volunteerhomestate,
                                 self.volunteerhomestate)


class Issue(models.Model):
    """A categorization scheme. This could eventually house relationships with
    individual projects, but for now, just point to sector funds"""
    name = models.CharField(max_length=NAME_LENGTH)
    icon = models.FileField(    # No need for any of the 'Media' fields
        help_text="Icon commonly used to represent this issue",
        upload_to='icons', validators=[svg.full_validation])
    icon_background = models.FileField(
        help_text="Background used when a large icon is present")
    campaigns = models.ManyToManyField(
        Campaign, limit_choices_to={'campaigntype': Campaign.SECTOR})

    def __str__(self):
        return self.name

    def projects(self):
        """Jump through the campaigns connection to get to a set of projects"""
        campaigns = self.campaigns.all()
        return Project.published_objects.filter(campaigns__in=campaigns)

    def icon_color(self, color):
        """Relative path to a colored version of the icon"""
        if self.icon:
            prefix, suffix = self.icon.name[:-4], self.icon.name[-4:]
            return prefix + '-' + color + suffix
        return ""

    def icon_color_url(self, color):
        """Full url to a colored version of the icon"""
        return self.icon.storage.url(self.icon_color(color))

    def save(self, *args, **kwargs):
        """Save other colors of the issue icon. We assume it is validated in
        the clean function"""
        if self.icon:
            xml = svg.validate_svg(self.icon.file.read())
            square = svg.make_square(xml)
            colors = svg.color_icon(square)
            super(Issue, self).save(*args, **kwargs)
            for key, content in colors.items():
                filename = self.icon_color(key)
                if self.icon.storage.exists(filename):
                    self.icon.storage.delete(filename)
                self.icon.storage.save(filename, svg.as_file(content))
        else:
            super(Issue, self).save(*args, **kwargs)


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


class FAQ(models.Model):
    question = models.CharField(max_length=256)
    answer = BraveSirTrevorField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    slug = models.SlugField(max_length=50, help_text="anchor", blank=True,
                            null=True)

    class Meta(object):
        ordering = ('order', )

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)[:50]
        super(FAQ, self).save(*args, **kwargs)
