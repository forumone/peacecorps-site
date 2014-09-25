from django.shortcuts import render
from django.http import HttpResponseRedirect

from peacecorps.forms import DedicationForm, IndividualDonationForm
from peacecorps.forms import OrganizationDonationForm


def donation_payment_individual(request):
    """ This is the view for the donations contact information form. """
    if request.method == 'POST':
        form = IndividualDonationForm(request.POST)
        dedication_form = DedicationForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/donations/review/')
    else:
        form = IndividualDonationForm()
        dedication_form = DedicationForm()
    return render(request, 'donations/donation_payment.jinja',
        {'form': form, 'dedication_form': dedication_form})

def donation_payment_organization(request):
    if request.method == 'POST':
        form = OrganizationDonationForm(request.POST)
        dedication_form = DedicationForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/donations/review')
    else:
        form = OrganizationDonationForm(initial={'donor_type':'Organization'})
        dedication_form = DedicationForm()
    return render(request, 'donations/donation_payment.jinja',
        {   
            'form': form,
            'organization': True,
            'dedication_form': dedication_form 
        })
