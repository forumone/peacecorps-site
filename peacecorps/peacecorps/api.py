import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from restless.http import Http400
from restless.models import serialize
from restless.modelviews import DetailEndpoint
from restless.views import Endpoint

from peacecorps.forms import DonationAmountForm, DonationPaymentForm
from peacecorps.models import Account, Campaign, Project
from peacecorps.payxml import convert_to_paygov


def _serialize_volunteer(project):
    """Pull out fields related to a volunteer into a dict"""
    if project.volunteerpicture:
        picture = project.volunteerpicture.url
    else:
        picture = None
    return {'name': project.volunteername,
            'homestate': project.volunteerhomestate,
            'picture': picture}


def _serialize_account(project):
    """Generate several useful fields related to a project's account"""
    account = project.account
    return {'goal': account.goal,
            'community_contribution': account.community_contribution,
            'total_donated': account.total_donated(),
            'total_raised': account.total_raised(),
            'total_cost': account.total_cost(),
            'percent_raised': account.percent_raised(),
            'percent_community': account.percent_community(),
            'funded': account.funded(),
            'remaining': account.remaining()}


def _serialize_overflow(project):
    """Overflow url for a project; path depends on the account type"""
    if project.overflow:
        if project.overflow.category == Account.PROJECT:
            view_name = 'donate project'
        else:
            view_name = 'donate campaign'
        return reverse(
            view_name,
            kwargs={'slug': project.overflow.project_or_fund().slug})
    return None


def _serialize_description(project):
    """The description content is stored as JSON. Kind of silly to deserialize
    and then serialize, but oh well"""
    try:
        return json.loads(project.description)
    except ValueError:
        return None


class ProjectDetail(DetailEndpoint):
    model = Project     # @todo - reduce number of queries
    lookup_field = 'slug'

    def serialize(self, obj):
        """The idealized project is a bit different than the DB model"""
        return serialize(
            obj,
            fields=(
                'title',
                'tagline',
                ('description', _serialize_description),
                ('volunteer', _serialize_volunteer),
                ('country', lambda o: o.country.name),
                ('account', _serialize_account),
                ('overflow', _serialize_overflow),
                ('featured_image',
                    lambda o: o.featured_image.url if o.featured_image
                    else None),
            ),

        )


class AbstractDonation(Endpoint):
    """Base class for fund and project donations; contains all of the form
    validation checks. @todo this duplicates a lot of the views functionality;
    the views should be calling here instead"""
    def serialize_errors(self, form):
        """Taken from django's as_json"""
        return {f: e.get_json_data() for f, e in form.errors.items()}

    def errors_or_paygov(self, account, data, host):
        """Return a 400 or the paygov data"""
        amount_form = DonationAmountForm(data, account=account)
        if not amount_form.is_valid():
            errors = self.serialize_errors(amount_form)
            return Http400(
                "validation error", error_form="amount", errors=errors)
        donorinfo_form = DonationPaymentForm(data)
        if not donorinfo_form.is_valid():
            errors = self.serialize_errors(donorinfo_form)
            return Http400(
                "validation error", error_form="donorinfo", errors=errors)

        # convert to cents
        payment_amount = int(amount_form.cleaned_data['payment_amount'] * 100)

        payment_data = dict(donorinfo_form.cleaned_data)
        payment_data['payment_amount'] = payment_amount
        payment_data['project_code'] = account.code
        paygov = convert_to_paygov(payment_data, account, "https://" + host)
        paygov.save()
        return {
            "agency_id": settings.PAY_GOV_AGENCY_ID,
            "agency_tracking_id": paygov.agency_tracking_id,
            "app_name": settings.PAY_GOV_APP_NAME,
            "oci_servlet_url": settings.PAY_GOV_OCI_URL,
        }


class ProjectDonation(AbstractDonation):
    def post(self, request, slug):
        project = get_object_or_404(
            Project.published_objects.select_related('account'),
            slug=slug)
        return self.errors_or_paygov(project.account, request.data,
                                     request.get_host())


class FundDonation(AbstractDonation):
    def post(self, request, slug):
        campaign = get_object_or_404(
            Campaign.objects.select_related('account'),
            slug=slug)
        return self.errors_or_paygov(campaign.account, request.data,
                                     request.get_host())
