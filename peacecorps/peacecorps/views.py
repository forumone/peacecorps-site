from datetime import datetime
from urllib.parse import urlencode
from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from peacecorps.forms import DonationAmountForm, DonationPaymentForm
from peacecorps.models import FeaturedIssue, FeaturedProjectFrontPage, Issue
from peacecorps.models import Project


def humanize_amount(amount_cents):
    """ Return a string that presents the donation amount in a humanized
    format. """

    amount_dollars = amount_cents/100.0
    return "$%.2f" % (amount_dollars)


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

    readable_amount = humanize_amount(amount)

    if request.method == 'POST':
        form = DonationPaymentForm(request.POST)

        if form.is_valid():
            data = {}
            for k, v in form.cleaned_data.items():
                data[k] = v
            return donation_payment_review(request, data)
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


def generate_agency_tracking_id():
    """ Generate an agency tracking ID for the transaction that has some random
    component. I include the date in here too, in case that's useful. (The
    current non-random tracking id has the date in it. """

    random = str(uuid4()).replace('-', '')
    today = datetime.now().strftime("%m%d")
    return 'PCOCI%s%s' % (today, random[0:6])


def generate_agency_memo(data):
    """Build the memo field from selections on the form"""
    memo = ''
    memo += '(' + data.get('comments', '').strip() + ')'
    memo += '(' + data.get('phone_number', '').strip() + ')'

    amount = humanize_amount(data['payment_amount'])
    memo += '(%s, %s)' % (data['project_code'], amount)

    if data.get('information_consent', '') == 'vol-consent-yes':
        memo += '(yes)'
    else:
        memo += '(no)'

    if data.get('interest_conflict'):
        memo += '(yes)'
    else:
        memo += '(no)'

    if data.get('email_consent'):
        memo += '(yes)'
    else:
        memo += '(no)'

    return memo


def generate_custom_fields(data):
    """Return a dictionary composed of 'custom' fields, formatted the way we
    expect."""
    custom = {}
    custom['custom_field_1'] = '(' + data.get('phone_number', '') + ')'
    custom['custom_field_1'] += '(' + data.get('email', '') + ')'
    custom['custom_field_2'] = '(' + data.get('billing_address', '') + ')'

    custom['custom_field_3'] = '(' + data.get('billing_city', '') + ')'
    custom['custom_field_3'] += '(' + data.get('billing_state', '') + ')'
    custom['custom_field_3'] += '(' + data.get('billing_zip', '') + ')'
    custom['custom_field_4'] = '(' + data.get('organization_name', '') + ')'

    custom['custom_field_5'] = '(' + data.get('dedication_name', '') + ')'
    custom['custom_field_5'] += '(' + data.get('dedication_contact', '') + ')'
    custom['custom_field_5'] += '(' + data.get('dedication_email', '') + ')'

    if data.get('dedication_type') == 'in-memory':
        custom['custom_field_6'] = '(Memory)'
    else:
        custom['custom_field_6'] = '(Honor)'
    if data.get('dedication_consent') == 'no-dedication-consent':
        custom['custom_field_6'] += '(no)'
    else:
        custom['custom_field_6'] += '(yes)'
    custom['custom_field_6'] += '(' + data.get('card_dedication', '') + ')'
    custom['custom_field_7'] = '(' + data.get('dedication_address', '') + ')'
    return custom


def donation_payment_review(request, data):
    """ This view is for a simple donation payment review page. """
    generate_custom_fields(data)

    return render(
        request,
        'donations/review_payment.jinja',
        {
            'data': data,
            'agency_memo': generate_agency_memo(data),
            'agency_id': settings.PAY_GOV_AGENCY_ID,
            'tracking_id': generate_agency_tracking_id(),
            'app_name': settings.PAY_GOV_APP_NAME,
            'oci_servlet_url': settings.PAY_GOV_OCI_URL,
        })


def donate_landing(request):

    featuredprojects = FeaturedProjectFrontPage.objects.select_related(
        'project__featured_image').all()

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
            'projects': Project.objects.all(),
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
        form = DonationAmountForm(data=request.POST, fund=project.fund)
        if form.is_valid():
            params = {'project': project.fund.fundcode,
                      # convert back into cents
                      'amount': 100*form.cleaned_data['payment_amount']}
            return HttpResponseRedirect(
                reverse('donations_payment') + '?' + urlencode(params))
    else:
        form = DonationAmountForm(fund=project.fund)

    return render(
        request,
        'donations/donate_project.jinja',
        {
            'project': project, 'form': form
        })
