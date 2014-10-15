from django.db import models
from localflavor.us.models import USPostalCodeField


def percentfunded(current, goal):
    try:
        return round((current/goal)*100,2)
    except ZeroDivisionError:
        return 0


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
    FUNDTYPE_CHOICES=(
        (COUNTRY, 'Country'),
        (SECTOR, 'Sector'),
        (MEMORIAL, 'Memorial'),
        (OTHER, 'Other'),
        (PROJECT,'Project'),
    )

    name = models.CharField(max_length=120)
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
    author = models.ForeignKey(
        'Volunteer', related_name="media", blank=True, null=True)
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


class Project(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(
        max_length=240, help_text="a short description for subheadings.")
    volunteer = models.ForeignKey('Volunteer')
    slug = models.SlugField(max_length=100, help_text="for the project url.")
    description = models.TextField(help_text="the full description.")
    country = models.ForeignKey('Country', related_name="projects")
    issue = models.ForeignKey('Issue', related_name="projects")
    issues_related = models.ManyToManyField(
        'Issue', related_name="related_projects",
        help_text="other issues this project relates to.")
    featured_image = models.ForeignKey(
        'Media',
        help_text="A large landscape image for use in banners, headers, etc")
    media = models.ManyToManyField(
        'Media', related_name="projects", blank=True, null=True)
    fund = models.ForeignKey('Fund', unique=True)
    # This one can't be its own table because Django doesn't do OneToMany.
    issue_feature = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    HE = "H"
    SHE = "S"
    THEY = "T"
    PRONOUN_CHOICES = (
        (HE, 'He'),
        (SHE, 'She'),
        (THEY, 'They'),
    )

    name = models.CharField(max_length=100)
    pronouns = models.CharField(
        max_length=2, choices=PRONOUN_CHOICES, default=THEY)
    profile_image = models.ForeignKey(
        'Media', related_name="volunteer", blank=True, null=True)
    homestate = USPostalCodeField(blank=True, null=True)
    homecity = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return '%s - %s, %s' % (self.name, self.homecity, self.homestate)
