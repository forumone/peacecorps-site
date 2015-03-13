# @todo split this file up, perhaps into smaller apps?
from datetime import timedelta
import json
import tempfile
import os

from django.conf import settings
from django.core.urlresolvers import reverse
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
    description field, where the description field is sir-trevor json. Also
    assumes that the object has a primary_url method (for the read-more
    link)."""

    def abstract_plaintext(self, include_shortened=False):
        """If an explicit abstract is present, return it. Otherwise, return
        the first paragraph of the description"""
        text = ''
        shortened = False
        if self.abstract:
            text = self.abstract
        elif self.description:
            for block in json.loads(self.description)['data']:
                if block.get('type') == 'text':
                    data = block['data']
                    # Naive string shortener
                    if len(data['text']) > settings.ABSTRACT_LENGTH:
                        trimmed = data['text'][:settings.ABSTRACT_LENGTH]
                        trimmed = trimmed[:trimmed.rindex(' ')]
                        text = trimmed
                        shortened = True
                    else:
                        text = data['text']
                    break
        if include_shortened:
            return text, shortened
        else:
            return text

    def abstract_html(self, read_more_link=False):
        """Take the plaintext and run it through a sir trevor template"""
        text, shortened = self.abstract_plaintext(include_shortened=True)
        context = {'text': text, 'shortened': shortened}
        if shortened and read_more_link:
            context['more_url'] = self.primary_url()
        return django_render('donations/includes/abstract.html', context)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(
            published=True)


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

    name = models.CharField(max_length=NAME_LENGTH, unique=True,
        help_text="The name of the project or fund.")
    code = models.CharField(max_length=25, primary_key=True,
        help_text="The accounting code for the project or fund.")
    current = models.IntegerField(
        default=0,
        help_text="Amount from donations (excluding real-time contributions), \
        in cents.")
    goal = models.IntegerField(
        blank=True, null=True,
        help_text="For PCPP projects, the funding goal, excluding community \
        contribution.")
    # @todo does it make sense for this to default zero?
    community_contribution = models.IntegerField(blank=True, null=True, 
        help_text="For PCPP projects, the amount of community contributions, \
        in cents.")
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, help_text="The type of \
        account.")

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


# @todo: Probably worth renaming
class Campaign(models.Model, AbstractHTMLMixin):
    """
    A campaign is any fundraising effort. Campaigns collect donations to a
    separate account that can be distributed to projects (sector, country,
    special, and memorial funds, the general fund).
    """
    COUNTRY = 'coun'
    GENERAL = 'gen'
    MEMORIAL = 'mem'
    OTHER = 'oth'
    SECTOR = 'sec'
    CAMPAIGNTYPE_CHOICES = (
        (COUNTRY, 'Country'),
        (GENERAL, 'General'),
        (SECTOR, 'Sector'),
        (MEMORIAL, 'Memorial'),
        (OTHER, 'Other'),
    )

    name = models.CharField(max_length=NAME_LENGTH, 
        help_text="The title for the associated campaign.")
    account = models.ForeignKey('Account', unique=True, 
        help_text="The accounting code for this campaign.")
    campaigntype = models.CharField(
        max_length=10, choices=CAMPAIGNTYPE_CHOICES,
        help_text="The type of campaign.",
        verbose_name="Campaign Type")
    icon = models.ForeignKey(
        'Media', null=True, blank=True, related_name="campaign-icons",
        help_text="Used for Memorial Funds. Typically a picture of the \
        volunteer. Should be 120px tall and 120px wide, with the focus of the \
        photo centered.",
        verbose_name="Memorial Fund Volunteer Image")
    featured_image = models.ForeignKey(
        'Media', null=True, blank=True, related_name="campaign-headers",
        help_text="A large landscape image for use at the top of the campaign \
        page. Should be 1100px wide and 454px tall.")
    tagline = models.CharField(
        max_length=140,
        help_text="If the campaign is featured on the home page, this text is \
        used as the description of the campaign.",
        blank=True, null=True)
    call = models.CharField(
        max_length=50, help_text="If the campaign is featured on the home \
        page, this text is used in the button as a Call to Action.",
        blank=True, null=True)
    slug = models.SlugField(
        help_text="Auto-generated. Used for the campaign page URL.",
        max_length=NAME_LENGTH, unique=True)
    description = BraveSirTrevorField(help_text="A rich text description. \
        of the campaign.")
    featuredprojects = models.ManyToManyField('Project', blank=True, null=True)
    country = models.ForeignKey(
        'Country', related_name="campaign", blank=True, null=True, unique=True,
        help_text="If the campaign is related to a specific country, the ID \
        of that country.")
    abstract = models.TextField(blank=True, null=True, max_length=256,
        help_text="A shorter description, used for quick views of the \
        campaign.")

    # Unlike projects, funds start published
    published = models.BooleanField(default=True, help_text="If published, \
        the project will be publicly visible on the site.")

    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return '%s: %s' % (self.account_id, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        """Save images to the Media model"""
        imagesave(self.description)

        super(Campaign, self).save(*args, **kwargs)

    def primary_url(self):
        if self.slug:
            return reverse('donate campaign', kwargs={'slug': self.slug})
        else:
            return reverse('donate projects funds')


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

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)


class FeaturedCampaign(models.Model):
    campaign = models.ForeignKey('Campaign', to_field='account',
                                 limit_choices_to={'published': True},
                                 help_text="The campaign to feature.")
    image = models.ForeignKey(
        'Media', help_text='Image shown on the landing page. 1100px \
        wide by 475px tall.')

    class Meta:
        verbose_name = 'Featured Campaign'
        verbose_name_plural = 'Featured Campaign'   # There is no plural

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
    image = models.ForeignKey(
        'Media', help_text='Image shown on the landing page. Roughly 525x320')

    class Meta:
        verbose_name = 'Featured Project'
        verbose_name_plural = 'Featured Projects'

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
        max_length=3, choices=MEDIATYPE_CHOICES, default=IMAGE,
        verbose_name="Media Type")
    caption = models.TextField(blank=True, null=True)
    country = models.ForeignKey('Country', blank=True, null=True,
        help_text="The country the photo was taken in.")
    description = models.TextField(
        help_text="Provide an image description for users with screenreaders. \
        If the image has text, transcribe the text here. If it's a image, \
        briefly describe what it depicts. Do not use HTML formatting.")
    transcript = models.TextField(
        help_text="If the media is a video or audio recording, transcribe it \
        for users with disabilities.",
        blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Media'

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


class Project(models.Model, AbstractHTMLMixin):
    title = models.CharField(max_length=NAME_LENGTH,
        help_text="The title of the project.")
    tagline = models.CharField(
        max_length=240, help_text="A short title, used as a subheading on the \
        home page.",
        blank=True, null=True)
    slug = models.SlugField(max_length=NAME_LENGTH,
                            help_text="Automatically generated, use for the \
                            project URL.")
    description = BraveSirTrevorField(help_text="A rich text description \
        of the project..")
    country = models.ForeignKey('Country', related_name="projects",
        help_text="The country the project is located in.")
    campaigns = models.ManyToManyField(
        'Campaign',
        help_text="The campaigns this project is related to.",
        blank=True, null=True)
    featured_image = models.ForeignKey(
        'Media', null=True, blank=True,
        help_text="A large landscape image for use on the project page. \
        Should be 1100px wide and 454px tall.")
    media = models.ManyToManyField(
        'Media', related_name="projects", blank=True, null=True)
    account = models.ForeignKey('Account', unique=True,
        help_text="The accounting code for the project.")
    overflow = models.ForeignKey(
        'Account', blank=True, null=True, related_name='overflow',
        help_text="The fund donors will be encourage to contribute to if the \
        project is fully funded. If no fund is selected, the default is the \
        project's sector fund.")
    volunteername = models.CharField(max_length=NAME_LENGTH,
        verbose_name="Volunteer Name",
        help_text="The name of the PCV requesting funds for the project.")
    volunteerpicture = models.ForeignKey(
        'Media', related_name="volunteer", blank=True, null=True,
        verbose_name="Volunteer Picture",
        help_text="A picture of the PCV requesting funds for the project. \
        Should be 175px by 175px.")
    volunteerhomestate = USPostalCodeField(blank=True, null=True,
        verbose_name="Volunteer Home State",
        help_text="The home state of the Volunteer.")
    abstract = models.TextField(blank=True, null=True,
        help_text="A shorter description, used for quick views of the \
        project.")

    # Unlike funds, projects start unpublished
    published = models.BooleanField(default=False, help_text="If selected, \
        the project will be visible to the public.")

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

    def primary_url(self):
        if self.slug:
            return reverse('donate project', kwargs={'slug': self.slug})
        else:
            return reverse('donate projects funds')


class Issue(models.Model):
    """A categorization scheme. This could eventually house relationships with
    individual projects, but for now, just point to sector funds"""
    name = models.CharField(max_length=NAME_LENGTH,
        help_text="The name of the issue.")
    icon = models.FileField(    # No need for any of the 'Media' fields
        help_text="An SVG file used to represent the issue.",
        upload_to='icons', validators=[svg.full_validation])
    icon_background = models.FileField(
        help_text="The background image to use behind the SVG icon. Should be \
        237px by 237px.")
    campaigns = models.ManyToManyField(
        Campaign, limit_choices_to={'campaigntype': Campaign.SECTOR},
        help_text="Sector funds to associate as being under this campaign.",
        verbose_name="Sector Funds")

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
    question = models.CharField(max_length=256, help_text="The question used \
        as the prompt for the FAQ.")
    answer = BraveSirTrevorField(help_text="The rich text answer to the \
        question.")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    slug = models.SlugField(max_length=50, help_text="The URL this \
        should exist at.", blank=True,
                            null=True)

    class Meta(object):
        ordering = ('order', )
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)[:50]
        super(FAQ, self).save(*args, **kwargs)
