from django import forms

from localflavor.us.forms import USStateField
from localflavor.us.forms import USStateSelect

from .countries import COUNTRY_OPTIONS


class DedicationForm(forms.Form):
    """ If the donation is being dedicated to someone, we use this form to
    validate and process """

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

    dedication_name = forms.CharField(
        label="Name", max_length=40, required=False)
    dedication_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DEDICATION_TYPE_CHOICES,
        initial='in-honor', required=False)
    #   @todo dedication_contact (present if "in memory")
    dedication_email = forms.EmailField(label="Email", required=False)
    dedication_address = forms.CharField(
        label="Mailing Address", max_length=255, required=False)
    card_dedication = forms.CharField(max_length=150, required=False)
    dedication_consent = forms.ChoiceField(
        widget=forms.RadioSelect, initial='yes-dedication-consent',
        choices=DEDICATION_CONSENT_CHOICES, required=False)


class DonationPaymentForm(forms.Form):
    """ The base donation form. This contains fields common to both the
    individual and organization varities. """

    DONOR_TYPE_CHOICES = (
        ('Individual', 'Individual'),
        ('Organization', 'Organization'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('credit-card', 'Credit Card'),
        ('ach-bank-check', 'ACH Bank Check'),
    )

    VOLUNTEER_CONSENT_CHOICES = (
        ('vol-consent-yes', 'Share with Volunteer'),
        ('vol-consent-no', "Don't share with Volunteer")
    )

    COUNTRY_CHOICES = COUNTRY_OPTIONS

    donor_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DONOR_TYPE_CHOICES,
        initial='Individual')
    email = forms.EmailField(required=False)
    street_address = forms.CharField(label="Street Address *", max_length=80)
    city = forms.CharField(label="City *", max_length=40)
    state = USStateField(label="State *", widget=USStateSelect, required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, initial='USA')
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

    # Dedication related fields
    dedication = forms.BooleanField(initial=False, required=False)

    # User consents to stay informed about the Peace Corps.
    email_consent = forms.BooleanField(initial=True, required=False)

    # True if there might be a possible conflict of interest.
    interest_conflict = forms.BooleanField(initial=False, required=False)

    information_consent = forms.ChoiceField(
        widget=forms.RadioSelect, choices=VOLUNTEER_CONSENT_CHOICES,
        initial='vol-consent-yes')


class IndividualDonationForm(DonationPaymentForm):
    """ An actual donation form. This one is for individuals. """

    name = forms.CharField(label="Name *", max_length=100)


class OrganizationDonationForm(DonationPaymentForm):
    """ An actual organization form. This one is for organizations. """
    organization_name = forms.CharField(
        label='Organization Name *', max_length=40)
    organization_contact = forms.CharField(
        label='Contact Person *', max_length=100)
