from datetime import datetime

from django.test import TestCase

from peacecorps.views import generate_agency_tracking_id

class DonationsTests(TestCase):
    def test_generate_agency_tracking_id(self):
        tracking_id = generate_agency_tracking_id()
        self.assertTrue(tracking_id.startswith('PCOCI'))

    def test_review_page(self):
        session = self.client.session
        session['name'] = 'William Williams'
        session['street_address'] = '1 Main Street' 
        session['city'] = 'Anytown'
        session['state'] =  'MD'
        session['zip_code'] = '20852'
        session['country'] = 'USA' 

        response = self.client.get('/donations/review')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('agency_tracking_id' in content)
        self.assertTrue('PCOCI' in content)
        self.assertTrue('app_name' in content)
        self.assertTrue('agency_memo' in content)
