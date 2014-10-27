from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
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


class Country(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)


class CountryFund(models.Model):
    country = models.ForeignKey('Country', related_name="fund")
    fund = models.ForeignKey('Fund', unique=True)
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc",
        blank=True, null=True)
    slug = models.SlugField(
        help_text="used for the fund page url.",
        max_length=100, unique=True)
    description = tinymce_models.HTMLField()

    def save(self):
        # can't prepopulate slugfields from foreignkeys in the admin.
        self.slug = slugify(self.country.name)

        # avoid error on non-unique
        if CountryFund.objects.filter(
                slug=self.slug).exclude(id=self.id).exists():

            self.slug = self.country.code + '-' + self.country.name

        super(CountryFund, self).save()

    def __str__(self):
        return self.country.name


class FeaturedIssue(models.Model):
    issue = models.ForeignKey('Issue')

    # Much like the Highlander, there can be only one.
    def save(self):
        for issue in FeaturedIssue.objects.all():
            issue.delete()
        self.id = 1
        super(FeaturedIssue, self).save()

    def __str__(self):
        return '%s (Featured)' % (self.issue.name)


class FeaturedProjectFrontPage(models.Model):
    project = models.ForeignKey('Project')

    def __str__(self):
        return '%s (Featured)' % (self.project.title)


class Fund(models.Model):
    COUNTRY = 'coun'
    MEMORIAL = 'mem'
    OTHER = 'oth'
    PROJECT = 'proj'
    SECTOR = 'sec'
    FUNDTYPE_CHOICES = (
        (COUNTRY, 'Country'),
        (SECTOR, 'Sector'),
        (MEMORIAL, 'Memorial'),
        (OTHER, 'Other'),
        (PROJECT, 'Project'),
    )

    name = models.CharField(max_length=120, unique=True)
    fundcode = models.CharField(max_length=25)
    fundcurrent = models.IntegerField(default=0)
    fundgoal = models.IntegerField(blank=True, null=True)
    community_contribution = models.IntegerField(blank=True, null=True)
    fundtype = models.CharField(
        max_length=10, choices=FUNDTYPE_CHOICES)

    def __str__(self):
        return '%s' % (self.name)

    def percent_funded(self):
        return percentfunded(self.fundcurrent, self.fundgoal)

    def funded(self):
        if self.fundcurrent >= self.fundgoal:
            return True
        else:
            return False

    def remaining(self):
        """This will be expanded later, and may involve more complicated
        calculations. As such, we don't want it to be a property"""
        return self.fundgoal - self.fundcurrent


class FundDisplay(models.Model):
    """
    Non-monetary info associated with a fund. Used for special & general funds.
    """
    name = models.CharField(max_length=200)
    fund = models.ForeignKey('Fund', unique=True)
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc",
        blank=True, null=True)
    slug = models.SlugField(
        help_text="used for the fund page url.",
        max_length=100, unique=True)
    description = tinymce_models.HTMLField()

    def __str__(self):
        return '%s' % (self.name)


class Issue(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(
        max_length=140,
        help_text="a short phrase for banners (140 characters)")
    call = models.CharField(
        max_length=40, help_text="call to action for buttons (40 characters)")
    description = models.TextField()
    slug = models.SlugField(
        help_text="used for the issue page url.",
        max_length=100, unique=True)
    icon = models.FileField(blank=True, null=True)  # TODO: Configure
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc")
    fund = models.ForeignKey('Fund', unique=True)

    def __str__(self):
        return '%s' % (self.name)


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

class MemorialFund(models.Model):
    name = models.CharField(max_length=200)
    fund = models.ForeignKey('Fund', unique=True)
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc",
        blank=True, null=True)
    headshot = models.ForeignKey(
        'Media',
        help_text="A picture of the memorialized person",
        related_name="memorial_headshot",
        blank=True, null=True)
    slug = models.SlugField(
        help_text="used for the fund page url.",
        max_length=100, unique=True)
    description = tinymce_models.HTMLField()

    def __str__(self):
        return '%s' % (self.name)

class Project(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(
        max_length=240, help_text="a short description for subheadings.")
    slug = models.SlugField(max_length=100, help_text="for the project url.")
    description = tinymce_models.HTMLField(help_text="the full description.")
    country = models.ForeignKey('Country', related_name="projects")
    issue = models.ForeignKey('Issue', related_name="projects")
    issues_related = models.ManyToManyField(
        'Issue', related_name="related_projects",
        help_text="other issues this project relates to.",
        blank=True, null=True)
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc")
    media = models.ManyToManyField(
        'Media', related_name="projects", blank=True, null=True)
    fund = models.ForeignKey('Fund', unique=True)
    # This one can't be its own table because Django doesn't do OneToMany.
    issue_feature = models.BooleanField(default=False)
    volunteername = models.CharField(max_length=100)
    volunteerpicture = models.ForeignKey(
        'Media', related_name="volunteer", blank=True, null=True)
    volunteerhomestate = USPostalCodeField(blank=True, null=True)
    volunteerhomecity = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.title


def default_expire_time():
    return timezone.now() + timedelta(minutes=settings.DONOR_EXPIRE_AFTER)


class DonorInfo(models.Model):
    """Represents a blob of donor information which will be requested by
    pay.gov. We need to limit accessibility as it contains PII"""
    agency_tracking_id = models.CharField(max_length=21, primary_key=True)
    fund = models.ForeignKey(Fund, related_name='donorinfos')
    xml = GPGField()
    expires_at = models.DateTimeField(default=default_expire_time)


class Donation(models.Model):
    """Log donation amounts as received from pay.gov"""
    fund = models.ForeignKey(Fund, related_name='donations')
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now=True)
