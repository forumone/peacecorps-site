from django.test import TestCase
from peacecorps.forms import IndividualDonationForm

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
            'information_consent': 'vol-consent-yes'
        }
        form = IndividualDonationForm(data=form_data)
        form_validity = form.is_valid()
        self.assertTrue(form.is_valid())
