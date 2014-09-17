from django import forms
from localflavor.us.forms import USPhoneNumberField, USStateField
from localflavor.us.forms import USZipCodeField, USStateSelect


class DonationPaymentForm(forms.Form):
    
    DONOR_TYPE_CHOICES = (
        ('Individual', 'Individual'),
        ('Organization', 'Organization'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('credit-card', 'Credit Card'), 
        ('ach-bank-check', 'ACH Bank Check'),
    )
    
    donor_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DONOR_TYPE_CHOICES,
        initial='Individual')
    name = forms.CharField(label="Name *", max_length=100)
    email = forms.EmailField(required=False)
    street_address = forms.CharField(label="Street Address *", max_length=80)
    city = forms.CharField(label="City *", max_length=40)
    payment_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_TYPE_CHOICES, 
        initial="credit-card",
    )
    comments = forms.CharField(max_length=150, required=False)

class USDonationPaymentForm(DonationPaymentForm):
    """ A US address specific donation payment form. Since most of the donors
    will likely reside in the United States, this makes sense. """

    state = USStateField(label="State *", widget=USStateSelect)
    zip_code = USZipCodeField()
    phone_number = USPhoneNumberField(required=False)
