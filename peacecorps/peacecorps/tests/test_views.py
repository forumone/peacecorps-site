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
        """The data dictionary should be serialized in the predictable way.
        Allow all fields to be optional"""
        """ This is really a placeholder test for when we have a better
        agency memo generator function. Currently, we check to see if the
        phone number is included. """
        data = {'comments': 'CCCCCC', 'phone_number': '5555555555',
                'information_consent': 'vol-consent-yes',
                'interest_conflict': True, 'email_consent': True}
        memo = generate_agency_memo(data)
        self.assertEqual("(CCCCCC)(5555555555)()(yes)(yes)(yes)", memo)

        memo = generate_agency_memo({})
        self.assertEqual("()()()(no)(no)(no)", memo)
