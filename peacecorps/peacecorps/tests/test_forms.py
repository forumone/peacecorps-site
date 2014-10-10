from django.test import TestCase
from peacecorps.forms import DonationPaymentForm


class DonationPaymentTests(TestCase):
    def form_data(self, clear=[], **kwargs):
        """Create a form_data object with reasonable defaults"""
        form_data = {
            'donor_type': 'Individual',
            'name': 'William Williams',
            'billing_address': '1 Main Street',
            'city': 'Anytown',
            'country': 'USA',
            'state': 'MD',
            'zip_code': '20852',
            'payment_type': 'CreditCard',
            'project_code': '15-4FF',
            'donation_amount': '3000',
            'information_consent': 'vol-consent-yes'
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
            clear=['name'], donor_type='Organization',
            organization_name='Big Corporation',
            organization_contact='Mr A.  Suit')
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_individual_requirements(self):
        """Verify that "name" is required if donor_type is Individual.
        Further, verify that the organization fields get cleared"""
        form_data = self.form_data(
            clear=['name'], organization_name='Big Corporation',
            organization_contact='Mr A. Suit')
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['name'] = 'Bob'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse('organization_name' in form.cleaned_data)
        self.assertFalse('organization_contact' in form.cleaned_data)

    def test_organization_requirements(self):
        """Verify that "organization_name" and "organization_contact" are
        required if donor_type is Organization. Also verify that the
        (Individual's) name field gets cleared"""
        form_data = self.form_data(donor_type='Organization')
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['organization_name'] = 'Org org'
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data['organization_contact'] = 'Contact'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse('name' in form.cleaned_data)

    def test_zip_state_requirements(self):
        """Zip code and state are only required when the country is the US"""
        form_data = self.form_data(clear=['state', 'zip_code'])
        form = DonationPaymentForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['country'] = 'CAN'
        form = DonationPaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
