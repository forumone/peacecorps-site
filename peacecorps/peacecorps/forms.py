from django import forms
from django.core.exceptions import ValidationError
from localflavor.us.us_states import STATE_CHOICES

from .models import Country
from .templatetags.humanize_cents import humanize_cents


class DonationPaymentForm(forms.Form):
    """Collect contact information and dedication information about a donor"""

    PAYMENT_TYPE_CHOICES = (
        ('CreditCard', 'Credit Card'),
        ('CreditACH', 'ACH Bank Check'),
    )

    is_org = forms.BooleanField(
        label="I'm donating on behalf of my organization", required=False)
    #   Will be hidden if "Organization" is selected
    payer_name = forms.CharField(
        label="Name", max_length=100, required=False,
        error_messages={'required': 'Please enter your full name'})
    #   Will be hidden in "Individual is selected"
    organization_name = forms.CharField(
        label='Organization Name', max_length=40, required=False)
    organization_contact = forms.CharField(
        label='Contact Person', max_length=100, required=False)

    email = forms.EmailField(required=False)
    # Be sure that country is processed before billing_state/zip
    country = forms.ModelChoiceField(
        queryset=Country.objects, to_field_name='code', initial='USA')
    billing_address = forms.CharField(
        label="Street Address", max_length=80,
        error_messages={'required': 'Please enter a valid address'})
    billing_address_extra = forms.CharField(
        label="Street Address (cont)", max_length=80, required=False)
    billing_city = forms.CharField(
        label="City", max_length=40,
        error_messages={'required': 'Please enter a valid city'})
    billing_state = forms.ChoiceField(
        label="State", choices=((('', ''),) + STATE_CHOICES), required=False)
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
        ('in-honor', 'in honor'),
        ('in-memory', 'in memory')
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
    card_dedication = forms.CharField(
        max_length=150, required=False,
        widget=forms.Textarea(attrs={'rows': 2}))
    dedication_consent = forms.ChoiceField(
        widget=forms.RadioSelect, initial='yes-dedication-consent',
        choices=DEDICATION_CONSENT_CHOICES, required=False)

    # User consents to stay informed about the Peace Corps.
    email_consent = forms.BooleanField(initial=True, required=False)

    # True if there might be a possible conflict of interest.
    interest_conflict = forms.BooleanField(initial=False, required=False)

    information_consent = forms.BooleanField(
        label='Make my contact info available to the volunteer',
        required=False, initial=True)

    def required_when(self, guard_field, guard_value, check_field, field_name):
        """Raises a validation error when both the field with name guard_field
        is equal to guard_value and the field with name check_field is
        empty"""
        if (self.cleaned_data.get(guard_field) == guard_value
                and not self.cleaned_data.get(check_field)):
            raise ValidationError('Please enter ' + field_name)
        return self.cleaned_data.get(check_field)

    def clean_payer_name(self):
        return self.required_when(
            'is_org', False, 'payer_name', 'your full name')

    def clean_organization_name(self):
        return self.required_when(
            'is_org', True, 'organization_name', 'your organization\'s name')

    def clean_organization_contact(self):
        return self.required_when(
            'is_org', True, 'organization_contact',
            "your organization's contact")

    def clean_billing_state(self):
        """Can't use required_when because the country field returns a model"""
        country = self.cleaned_data.get('country')
        state = self.cleaned_data.get('billing_state')
        if country and country.code == 'USA' and not state:
            raise ValidationError('Please select a valid state')
        return state

    def clean_billing_zip(self):
        country = self.cleaned_data.get('country')
        zip = self.cleaned_data.get('billing_zip')
        if country and country.code == 'USA' and not zip:
            raise ValidationError('Please enter a valid zip code')
        return zip

    def clean(self):
        """Only one of the organization/individual set of fields should be
        present. Blank out the other"""
        if self.cleaned_data.get('is_org'):
            del self.cleaned_data['payer_name']
        else:
            del self.cleaned_data['organization_name']
            del self.cleaned_data['organization_contact']
        return self.cleaned_data


class DonationAmountForm(forms.Form):
    """Validation of donation amounts."""
    # bounds checks are performed in the clean_payment_amount method
    payment_amount = forms.DecimalField(decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        """Note that project_max, if present, is in cents while payment_amount
        is in dollars"""
        self.project_max = None
        account = kwargs.pop('account', None)
        if account and account.goal:
            self.project_max = account.remaining()
        super(DonationAmountForm, self).__init__(*args, **kwargs)

    def clean_payment_amount(self):
        """Check for bounds, including account-specific bounds"""
        if self.cleaned_data.get('payment_amount') is None:
            raise ValidationError(
                'Please fill in the amount you want to give', code='required')
        else:
            amount = self.cleaned_data.get('payment_amount')

        # Pay.gov doesn't process anything above $9,999.99
        if amount >= 10000:
            raise ValidationError(
                "Thank you for your generosity! While we can’t accept gifts "
                + "that large through the website, we would love to talk "
                + "with you about ways you can make that donation. Please "
                + "give us a call at 202-692-2170.", code='max_value')
        # Min value of $1, as anything lower than that will cost too much
        # money to process.
        elif amount < 1:
            raise ValidationError(
                "Sorry, we can't accept gifts of less than a dollar",
                code="min_value")
        # * 100 for cents
        elif self.project_max is not None and amount * 100 > self.project_max:
            raise ValidationError(
                "Whoops, that's more than we need for this project ("
                + humanize_cents(self.project_max) + " max)", code='max_value')
        return amount
