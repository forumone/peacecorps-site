from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from localflavor.us.forms import USStateField
from localflavor.us.forms import USStateSelect

from .countries import COUNTRY_OPTIONS


class DonationPaymentForm(forms.Form):
    """Collect contact information and dedication information about a donor"""

    DONOR_TYPE_CHOICES = (
        ('Individual', 'Individual'),
        ('Organization', 'Organization'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('CreditCard', 'Credit Card'),
        ('CreditACH', 'ACH Bank Check'),
    )

    VOLUNTEER_CONSENT_CHOICES = (
        ('vol-consent-yes', 'Share with Volunteer'),
        ('vol-consent-no', "Don't share with Volunteer")
    )

    COUNTRY_CHOICES = COUNTRY_OPTIONS

    donor_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DONOR_TYPE_CHOICES,
        initial='Individual')
    #   Will be hidden if "Organization" is selected
    payer_name = forms.CharField(label="Name", max_length=100, required=False)
    #   Will be hidden in "Individual is selected"
    organization_name = forms.CharField(
        label='Organization Name', max_length=40, required=False)
    organization_contact = forms.CharField(
        label='Contact Person', max_length=100, required=False)

    email = forms.EmailField(required=False)
    billing_address = forms.CharField(label="Street Address", max_length=80)
    billing_city = forms.CharField(label="City", max_length=40)
    billing_state = USStateField(
        label="State", widget=USStateSelect, required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, initial='USA')
    billing_zip = forms.CharField(required=False)
    phone_number = forms.CharField(required=False, max_length=15)
    payment_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_TYPE_CHOICES,
        initial="CreditCard",
    )
    comments = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}))

    # Dedication related fields - all except the first will only be visible if
    # dedication is True
    dedication = forms.BooleanField(initial=False, required=False)
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
    dedication_contact = forms.CharField(
        label="Family Contact", max_length=40, required=False)
    dedication_email = forms.EmailField(label="Email", required=False)
    dedication_address = forms.CharField(
        label="Mailing Address", max_length=255, required=False)
    card_dedication = forms.CharField(max_length=150, required=False)
    dedication_consent = forms.ChoiceField(
        widget=forms.RadioSelect, initial='yes-dedication-consent',
        choices=DEDICATION_CONSENT_CHOICES, required=False)

    # User consents to stay informed about the Peace Corps.
    email_consent = forms.BooleanField(initial=True, required=False)

    # True if there might be a possible conflict of interest.
    interest_conflict = forms.BooleanField(initial=False, required=False)

    information_consent = forms.ChoiceField(
        widget=forms.RadioSelect, choices=VOLUNTEER_CONSENT_CHOICES,
        initial='vol-consent-yes')

    payment_amount = forms.IntegerField(widget=forms.HiddenInput())
    project_code = forms.CharField(max_length=40, widget=forms.HiddenInput())

    def required_when(self, guard_field, guard_value, check_field):
        """Raises a validation error when both the field with name guard_field
        is equal to guard_value and the field with name check_field is
        empty"""
        if (self.cleaned_data.get(guard_field) == guard_value
                and not self.cleaned_data.get(check_field)):
            raise ValidationError('This field is required.')
        return self.cleaned_data.get(check_field)

    def clean_payer_name(self):
        return self.required_when('donor_type', 'Individual', 'payer_name')

    def clean_organization_name(self):
        return self.required_when('donor_type', 'Organization',
                                  'organization_name')

    def clean_organization_contact(self):
        return self.required_when('donor_type', 'Organization',
                                  'organization_contact')

    def clean_billing_state(self):
        return self.required_when('country', 'USA', 'billing_state')

    def clean_billing_zip(self):
        return self.required_when('country', 'USA', 'billing_zip')

    def clean(self):
        """Only one of the organization/individual set of fields should be
        present. Blank out the other"""
        if self.cleaned_data.get('donor_type') == 'Organization':
            del self.cleaned_data['payer_name']
        else:
            del self.cleaned_data['organization_name']
            del self.cleaned_data['organization_contact']
        return self.cleaned_data


class DonationAmountForm(forms.Form):
    """Validation of donation amounts."""
    presets = forms.ChoiceField(
        widget=forms.RadioSelect, initial='preset-25',
        choices=(('preset-10', '10.00'),
                 ('preset-25', '25.00'),
                 ('preset-50', '50.00'),
                 ('custom', 'Custom'),
                 ('preset-all', 'Fund the remaining amount')))
    # required if "custom" is selected above. Min value of $1, as anything
    # lower than that will cost too much money to process. Max value of
    # $10,000, as anything above that can't be processed by pay.gov
    payment_amount = forms.DecimalField(max_value=10000, min_value=1,
                                        decimal_places=2, required=False)

    def __init__(self, fund=None, *args, **kwargs):
        """We need a fund to set payment amount when preset-all is
        selected"""
        super(DonationAmountForm, self).__init__(*args, **kwargs)
        self.fund = fund

    def clean_payment_amount(self):
        """Selecting a preset is identical to typing the exact amount"""
        for amt in (10, 25, 50):
            if self.cleaned_data.get('presets') == 'preset-' + str(amt):
                return Decimal(amt)
        if self.cleaned_data.get('presets') == 'preset-all':
            if not self.fund:
                raise ValidationError('Missing fund')
            else:
                remaining_amount = self.fund.fundgoal - self.fund.fundcurrent
                # We're circumventing the normal bounds checks, so we must
                # enforce them here
                if remaining_amount < 100:  # cents
                    raise ValidationError('Must be >= 1.00')
                elif remaining_amount > 1000000:
                    raise ValidationError('Must be <= 10,000.00')
                return Decimal(remaining_amount / 100.00)  # user sees dollars

        raise ValidationError('This field is required.')
