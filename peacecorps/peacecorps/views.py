from urllib.parse import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from peacecorps.forms import DonationAmountForm, DonationPaymentForm
from peacecorps.models import CountryFund, FeaturedIssue
from peacecorps.models import FeaturedProjectFrontPage, Fund, humanize_amount
from peacecorps.models import Issue, Project
from peacecorps.payxml import convert_to_paygov


def donation_payment(request):
    """ Collect donor contact information. """

    amount = request.GET.get('amount', None)
    project_code = request.GET.get('project', None)

    if amount is None or project_code is None:
        return HttpResponseBadRequest(
            'amount and project must be provided.')
    try:
        amount = int(amount)
    except ValueError:
        return HttpResponseBadRequest('amount must be an integer value')

    fund = Fund.objects.filter(fundcode=project_code).first()
    if not fund:
        return HttpResponseBadRequest('Invalid project')

    readable_amount = humanize_amount(amount)

    if request.method == 'POST':
        form = DonationPaymentForm(request.POST)

        if form.is_valid():
            data = {}
            for k, v in form.cleaned_data.items():
                data[k] = v
            return donation_payment_review(request, data, fund)
    else:
        data = {'payment_amount': amount, 'project_code': project_code}
        form = DonationPaymentForm(initial=data)

    return render(
        request, 'donations/donation_payment.jinja',
        {
            'form': form,
            'amount': readable_amount,
            'project_code': project_code
        })


def donation_payment_review(request, data, fund):
    """Save the payment information for future access; provide the user with a
    form that sends them over to pay.gov"""
    paygov = convert_to_paygov(data, fund)
    paygov.save()

    return render(
        request,
        'donations/review_payment.jinja',
        {
            'data': data,
            'agency_id': settings.PAY_GOV_AGENCY_ID,
            'agency_tracking_id': paygov.agency_tracking_id,
            'app_name': settings.PAY_GOV_APP_NAME,
            'oci_servlet_url': settings.PAY_GOV_OCI_URL,
        })


def donate_landing(request):

    featuredprojects = FeaturedProjectFrontPage.objects.select_related(
        'project__featured_image').all()
    projects = Project.objects.select_related('country', 'fund')

    try:
        featuredissue = FeaturedIssue.objects.get(id=1).issue
    except FeaturedIssue.DoesNotExist:
        featuredissue = None

    return render(
        request,
        'donations/donate_landing.jinja',
        {
            'featuredissue': featuredissue,
            'issues': Issue.objects.all(),
            'featuredprojects': featuredprojects,
            'projects': projects,
            'humanize_amount': humanize_amount,
        })


def donate_issue(request, slug):

    issue = Issue.objects.select_related('fund').get(slug=slug)
    featured = Project.objects.filter(issue=issue, issue_feature=True)
    projects = Project.objects.filter(issue=issue)

    return render(
        request,
        'donations/donate_issue.jinja',
        {
            'issue': issue,
            'featured': featured,
            'projects': projects,
        })


def donate_project(request, slug):
    """A profile for each project. Also includes a donation form"""
    project = get_object_or_404(
        Project.objects.select_related('volunteer__profile_image',
                                       'featured_image', 'fund'),
        slug=slug)
    if request.method == 'POST':
        top_form = DonationAmountForm(prefix="top", data=request.POST,
                                      fund=project.fund)
        bottom_form = DonationAmountForm(prefix="bottom", data=request.POST,
                                         fund=project.fund)
        for form in (top_form, bottom_form):
            if form.is_valid():
                params = {'project': project.fund.fundcode,
                          # convert back into cents
                          'amount': int(form.cleaned_data['payment_amount']
                                        * 100)}
                return HttpResponseRedirect(
                    reverse('donations_payment') + '?' + urlencode(params))
    else:
        top_form = DonationAmountForm(prefix="top", fund=project.fund)
        bottom_form = DonationAmountForm(prefix="bottom", fund=project.fund)

    return render(
        request,
        'donations/donate_project.jinja',
        {
            'project': project,
            'top_form': top_form,
            'bottom_form': bottom_form,
        })


def donate_country(request, slug):
    """
    The page for the individual countries in which the Peace Corps operates.
    Users can donate to the country fund and see the list of active projects in
    that country.
    """
    country = CountryFund.objects.select_related(
        'featured_image', 'fund').get(slug=slug)
    projects = Project.objects.filter(country=country.country)

    return render(
        request,
        'donations/donate_country.jinja',
        {
            'country': country,
            'projects': projects,
        })


def donate_countries(request):
    """
    Page listing all of the countries in which the Peace Corps is active, with
    links to country pages.
    """
    countries = CountryFund.objects.select_related(
        'featured_image', 'fund').all()

    return render(
        request,
        'donations/donate_countries.jinja',
        {
            'countries': countries,
        })


def donation_success(request):
    """User returns here on a successful donation. Can be extended to lookup
    the project and redirect if needed."""
    return render(request, 'donations/success.jinja')


def donation_failure(request):
    """User returns here on a failed donation. Can be extended to lookup
    the project and redirect if needed."""
    return render(request, 'donations/failure.jinja')
