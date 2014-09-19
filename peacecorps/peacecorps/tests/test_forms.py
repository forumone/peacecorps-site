from django.test import TestCase
from peacecorps.forms import USDonationPaymentForm

class DonationPaymentTests(TestCase):
    def test_us_donation_required(self):
        form_data = {
            'donor_type': 'Individual',
            'name': 'William Williams',
            'street_address': '1 Main Street',
            'city': 'Anytown',
            'state': 'MD',
            'zip_code': '20852',
            'payment_type': 'credit-card',
            'information_consent': 'vol-consent-yes'
        }
        form = USDonationPaymentForm(data=form_data)
        form_validity = form.is_valid()
        print(form.errors)
        self.assertEqual(form.is_valid(), True)
