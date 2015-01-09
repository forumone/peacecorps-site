from decimal import Decimal

from django.test import TestCase

from peacecorps.models import Account, Country
from peacecorps.forms import DonationAmountForm, DonationPaymentForm


class DonationPaymentTests(TestCase):
    def setUp(self):
        Country.objects.create(code='USA', name='United States of America')
        Country.objects.create(code='CAN', name='Canada')

    def tearDown(self):
        Country.objects.all().delete()

    def form_data(self, clear=[], **kwargs):
        """Create a form_data object with reasonable defaults"""
        form_data = {
            'payer_name': 'William Williams',
            'billing_address': '1 Main Street',
            'billing_city': 'Anytown',
            'country': 'USA',
            'billing_state': 'MD',
            'billing_zip': '20852',
            'payment_type': 'CreditCard',
            'project_code': '15-4FF',
            'payment_amount': '3000',
            'information_consent': True,
        }
        for key in clear:
            del form_data[key]
        for key, value in kwargs.items():
            form_data[key] = value
        return form_data

    def test_individual_donation_required(self):
        """ Check the minimum required data.  """
        form_data = self.form_data()
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_individual_ACH(self):
        """" Set the payment_type to ACH and check validation. """
        form_data = self.form_data()
        form_data['payment_type'] = 'CreditACH'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_organization_donation_required(self):
        """ Check the minimum required data for the organization form. """
        form_data = self.form_data(
            clear=['payer_name'], is_org=True,
            organization_name='Big Corporation',
            organization_contact='Mr A.  Suit')
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_individual_requirements(self):
        """Verify that "name" is required if it is Individual.
        Further, verify that the organization fields get cleared"""
        form_data = self.form_data(
            clear=['payer_name'], organization_name='Big Corporation',
            organization_contact='Mr A. Suit')
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['payer_name'] = 'Bob'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse('organization_name' in form.cleaned_data)
        self.assertFalse('organization_contact' in form.cleaned_data)

    def test_organization_requirements(self):
        """Verify that "organization_name" and "organization_contact" are
        required if it is an Organization. Also verify that the
        (Individual's) name field gets cleared"""
        form_data = self.form_data(is_org=True)
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['organization_name'] = 'Org org'
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data['organization_contact'] = 'Contact'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse('payer_name' in form.cleaned_data)

    def test_zip_state_requirements(self):
        """Zip code and state are only required when the country is the US"""
        form_data = self.form_data(clear=['billing_state'])
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = self.form_data(billing_state='')
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = self.form_data(clear=['billing_zip'])
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = self.form_data(clear=['billing_state', 'billing_zip'])
        form_data['country'] = 'CAN'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())


class DonationAmountTests(TestCase):
    def test_preset_50(self):
        """Selecting a preset should set the correct value in
        payment_amount"""
        data = {'presets': 'preset-50'}
        form = DonationAmountForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['payment_amount'], Decimal(50))

    def test_preset_custom(self):
        """Entering no value will result in an error. Entering a custom amount
        will resolve"""
        data = {'presets': 'custom'}
        form = DonationAmountForm(data=data)
        self.assertFalse(form.is_valid())

        data['payment_amount'] = 1250
        form = DonationAmountForm(data=data)
        self.assertTrue(form.is_valid())

    def test_custom_required(self):
        """Payment amount of some form is required"""
        data = {'presets': 'custom'}
        form = DonationAmountForm(data=data)
        self.assertFalse(form.is_valid())
        errors = form.errors.as_data()
        self.assertTrue('payment_amount' in errors)
        self.assertEqual('required', errors['payment_amount'][0].code)

    def test_custom_lower_limit(self):
        data = {'presets': 'custom', 'payment_amount': '0.99'}
        form = DonationAmountForm(data=data)
        self.assertFalse(form.is_valid())
        errors = form.errors.as_data()
        self.assertEqual('min_value', errors['payment_amount'][0].code)

        data['payment_amount'] = '1.00'
        self.assertTrue(DonationAmountForm(data=data).is_valid())

    def test_custom_upper_limit(self):
        """Ceiling of 9999.99"""
        data = {'presets': 'custom', 'payment_amount': '10000'}
        form = DonationAmountForm(data=data)
        self.assertFalse(form.is_valid())
        errors = form.errors.as_data()
        self.assertEqual('max_value', errors['payment_amount'][0].code)

        data['payment_amount'] = '9999.99'
        self.assertTrue(DonationAmountForm(data=data).is_valid())

    def test_custom_per_project_upper_limit(self):
        """Error if trying to donate more than a project needs"""
        data = {'presets': 'preset-50'}
        account = Account(goal=8000, current=3001)
        form = DonationAmountForm(data=data, account=account)
        self.assertFalse(form.is_valid())
        errors = form.errors.as_data()
        self.assertEqual('max_value', errors['payment_amount'][0].code)
        self.assertTrue('$49.99' in errors['payment_amount'][0].message)

        account.current = 3000
        form = DonationAmountForm(data=data, account=account)
        self.assertTrue(form.is_valid())
