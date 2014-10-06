from django.test import TestCase
from peacecorps.forms import IndividualDonationForm, OrganizationDonationForm


class DonationPaymentTests(TestCase):
    def test_individual_donation_required(self):
        """ Check the minimum required data.  """
        form_data = {
            'donor_type': 'Individual',
            'name': 'William Williams',
            'street_address': '1 Main Street',
            'city': 'Anytown',
            'country': 'USA',
            'state': 'MD',
            'zip_code': '20852',
            'payment_type': 'credit-card',
            'project_code': '15-4FF',
            'donation_amount': '3000',
            'information_consent': 'vol-consent-yes'
        }
        form = IndividualDonationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_organization_donation_required(self):
        """ Check the minimum required data for the organization form. """

        form_data = {
            'donor_type': 'Organization',
            'organization_name': 'Big Corporation',
            'organization_contact': 'Mr A. Suit',
            'street_address': '1 Main Street',
            'city': 'Anytown',
            'country': 'USA',
            'state': 'MD',
            'zip_code': '20852',
            'project_code': '15-4FF',
            'donation_amount': '3000',
            'payment_type': 'credit-card',
            'information_consent': 'vol-consent-yes'
        }
        form = OrganizationDonationForm(data=form_data)
        self.assertTrue(form.is_valid())
