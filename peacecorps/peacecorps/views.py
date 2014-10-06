from uuid import uuid4
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from peacecorps.forms import DedicationForm, IndividualDonationForm
from peacecorps.forms import OrganizationDonationForm


def humanize_amount(amount_cents):
    """ Return a string that presents the donation amount in a humanized
    format. """

    amount_dollars = amount_cents/100.0
    return "$%.2f" % (amount_dollars)

def donation_payment_individual(request):
    """ This is the view for the donations contact information form. """

    amount = int(request.GET.get('amount', None))
    project_code = request.GET.get('project', None)

    if amount is None or project_code is None:
        return HttpResponseRedirect('/')

    readable_amount = humanize_amount(amount)

    if request.method == 'POST':
        form = IndividualDonationForm(request.POST)
        dedication_form = DedicationForm(request.POST)

        if form.is_valid():
            for k, v in form.cleaned_data.items():
                request.session[k] = v
            return HttpResponseRedirect('/donations/review')
    else:
        data = {'donation_amount': amount, 'project_code': project_code}
        form = IndividualDonationForm(initial=data)
        dedication_form = DedicationForm()

    return render(
        request, 'donations/donation_payment.jinja',
        {
            'form': form,
            'dedication_form': dedication_form,
            'amount': readable_amount,
            'project_code': project_code
        })


def donation_payment_organization(request):
    """ If the user is representing an organization, this is the relevant
    view. It uses an organization specific form. """
    if request.method == 'POST':
        form = OrganizationDonationForm(request.POST)
        dedication_form = DedicationForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/donations/review')
    else:
        form = OrganizationDonationForm(initial={'donor_type': 'Organization'})
        dedication_form = DedicationForm()
    return render(
        request, 'donations/donation_payment.jinja',
        {
            'form': form,
            'organization': True,
            'dedication_form': dedication_form
        })


def generate_agency_tracking_id():
    """ Generate an agency tracking ID for the transaction that has some random
    component. I include the date in here too, in case that's useful. (The
    current non-random tracking id has the date in it. """

    random = str(uuid4()).replace('-', '')
    today = datetime.now().strftime("%m%d")
    return 'PCOCI%s%s' % (today, random[0:6])


def generate_agency_memo(data):
    """ This currently returns a faked agency memo. Later we'll replace this.
    """
    phone = '()'
    if 'phone_number' in data:
        phone = '(%s)' % data['phone_number']

    amount = humanize_amount(data['donation_amount'])

    memo = '()(%s, %s/)' % (data[project_code], amount)
    memo += phone
    memo += '(yes)(no)(yes)'
    return memo


def donation_payment_review(request):
    """ This view is for a simple donation payment review page. """
    data = {}
    for k, v in request.session.items():
        data[k] = v

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
