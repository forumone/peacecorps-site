from django.shortcuts import render
from django.http import HttpResponseRedirect

from peacecorps.forms import DonationPaymentForm


def donation_payment_us(request):
    """ This is the view for the donations contact information form. """
    if request.method == 'POST':
        form = DonationPaymentForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/donations/review/')
    else:
        form = DonationPaymentForm()
    return render(request, 'donations/donation_payment.jinja', {'form': form})
