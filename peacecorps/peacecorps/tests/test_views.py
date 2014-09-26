from datetime import datetime

from django.test import TestCase

from peacecorps.views import generate_agency_tracking_id, generate_agency_memo


class DonationsTests(TestCase):
    def test_generate_agency_tracking_id(self):
        """ This just tests the start of a generated tracking id, which is
        currently the only piece we're sure of. """

        tracking_id = generate_agency_tracking_id()
        self.assertTrue(tracking_id.startswith('PCOCI'))

    def test_review_page(self):
        """ Test that the donation review page renders with the required
        elements. """

        session = self.client.session
        session['name'] = 'William Williams'
        session['street_address'] = '1 Main Street'
        session['city'] = 'Anytown'
        session['state'] = 'MD'
        session['zip_code'] = '20852'
        session['country'] = 'USA'

        response = self.client.get('/donations/review')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('agency_tracking_id' in content)
        self.assertTrue('PCOCI' in content)
        self.assertTrue('app_name' in content)
        self.assertTrue('agency_memo' in content)

    def test_generate_agency_memo(self):
        """ This is really a placeholder test for when we have a better
        agency memo generator function. Currently, we check to see if the
        phone number is included. """
        agency_memo = generate_agency_memo({'phone_number': '5555555'})
        self.assertTrue('5555555' in agency_memo)
