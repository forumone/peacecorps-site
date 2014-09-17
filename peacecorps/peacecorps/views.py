from django.shortcuts import render
from django.http import HttpResponseRedirect

from peacecorps.forms import USDonationPaymentForm


def donation_payment_us(request):
    """ This is the view for the donations contact information form. """
    if request.method == 'POST':
        form = USDonationPaymentForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = USDonationPaymentForm()
    return render(request, 'donations/donation_payment.jinja', {'form': form})
