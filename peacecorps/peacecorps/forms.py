from django import forms
from localflavor.us.forms import USStateField
from localflavor.us.forms import USStateSelect


class DonationPaymentForm(forms.Form):

    DONOR_TYPE_CHOICES = (
        ('Individual', 'Individual'),
        ('Organization', 'Organization'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('credit-card', 'Credit Card'),
        ('ach-bank-check', 'ACH Bank Check'),
    )

    DEDICATION_TYPE_CHOICES = (
        ('in-honor', 'In Honor'),
        ('in-memory', 'In Memory')
    )

    ded_yes = "I authorize the Peace Corps to make my name and contact"
    ded_yes += " information available to the honoree."

    ded_no = "I do not authorize the Peace Corps to make my name and contact"
    ded_no += " information available to the honoree."

    DEDICATION_CONSENT_CHOICES = (
        ('yes-dedication-consent', ded_yes),
        ('no-dedication-consent', ded_no),
    )

    VOLUNTEER_CONSENT_CHOICES = (
        ('vol-consent-yes', 'Share with Volunteer'),
        ('vol-consent-no', "Don't share with Volunteer")
    )

    donor_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DONOR_TYPE_CHOICES,
        initial='Individual')
    name = forms.CharField(label="Name *", max_length=100)
    organization_name = forms.CharField(
        label='Organization Name *', max_length=40, required=False)
    organization_contact = forms.CharField(
        label='Contact Person *', max_length=100, required=False)
    email = forms.EmailField(required=False)
    street_address = forms.CharField(label="Street Address *", max_length=80)
    city = forms.CharField(label="City *", max_length=40)
    state = USStateField(label="State *", widget=USStateSelect, required=False)
    zip_code = forms.CharField(required=False)
    phone_number = forms.CharField(required=False, max_length=15)
    payment_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_TYPE_CHOICES,
        initial="credit-card",
    )
    comments = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}))

    # User consents to stay informed about the Peace Corps.
    email_consent = forms.BooleanField(initial=True, required=False)

    # True if there might be a possible conflict of interest.
    interest_conflict = forms.BooleanField(initial=False, required=False)

    information_consent = forms.ChoiceField(
        widget=forms.RadioSelect, choices=VOLUNTEER_CONSENT_CHOICES,
        initial='vol-consent-yes')

    # Dedication related fields
    dedication = forms.BooleanField(initial=False, required=False)
    dedication_name = forms.CharField(
        label="Name", max_length=40, required=False)

    dedication_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DEDICATION_TYPE_CHOICES,
        initial='in-honor', required=False)
    dedication_email = forms.EmailField(label="Email", required=False)
    dedication_address = forms.CharField(
        label="Mailing Address", max_length=255, required=False)
    card_dedication = forms.CharField(max_length=150, required=False)
    dedication_consent = forms.ChoiceField(
        widget=forms.RadioSelect, initial='yes-dedication-consent',
        choices=DEDICATION_CONSENT_CHOICES, required=False)
