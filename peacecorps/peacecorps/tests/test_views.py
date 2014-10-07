from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.utils.importlib import import_module

from peacecorps.views import generate_agency_tracking_id, generate_agency_memo
from peacecorps.views import generate_custom_fields, humanize_amount


class SessionTestCase(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key


class DonationsTests(SessionTestCase):

    def test_generate_agency_tracking_id(self):
        """ This just tests the start of a generated tracking id, which is
        currently the only piece we're sure of. """

        tracking_id = generate_agency_tracking_id()
        self.assertTrue(tracking_id.startswith('PCOCI'))

    def test_contribution_parameters(self):
        """ To get to the page where name, address are filled out before being
        shunted to pay.gov we need to pass the donation amount and project code
        as GET parameters. This makes sure they show up on the payment page.
        """

        response = self.client.get(
            '/donations/contribute/individual?amount=2000&project=14-532-001')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('$20.00' in content)
        self.assertTrue('14-532-001')

    def test_review_page(self):
        """ Test that the donation review page renders with the required
        elements. """

        session = self.session
        session['name'] = 'William Williams'
        session['street_address'] = '1 Main Street'
        session['city'] = 'Anytown'
        session['state'] = 'MD'
        session['zip_code'] = '20852'
        session['country'] = 'USA'
        session['donation_amount'] = 2000
        session['project_code'] = 'PC-SEC01'
        session.save()

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
        data = {'comments': 'CCCCCC', 'phone_number': '5555555555',
                'information_consent': 'vol-consent-yes',
                'donation_amount': 2000, 'project_code': '14-54FF',
                'interest_conflict': True, 'email_consent': True}
        memo = generate_agency_memo(data)
        self.assertEqual(
            "(CCCCCC)(5555555555)(14-54FF, $20.00)(yes)(yes)(yes)", memo)

        memo = generate_agency_memo({
            'donation_amount': 2000, 'project_code': '14-54FF'})
        self.assertEqual("()()(14-54FF, $20.00)(no)(no)(no)", memo)

    def test_generate_custom_fields(self):
        """The data dictionary should be serialized in the predictable way.
        Allow all fields to be optional"""
        data = {'phone_number': '1112223333', 'email': 'aaa@example.com',
                'street_address': 'stttt', 'city': 'ccc', 'state': 'ST',
                'zip_code': '90210', 'organization_name': 'OOO',
                'dedication_name': 'Bob', 'dedication_contact': 'Patty',
                'dedication_email': 'family@example.com',
                'dedication_type': 'in-memory',
                'dedication_consent': 'no-dedication-consent',
                'card_dedication': 'Good Jorb',
                'dedication_address': '111 Somewhere'}

        self.assertEqual(generate_custom_fields(data), {
            'custom_field_1': '(1112223333)(aaa@example.com)',
            'custom_field_2': '(stttt)',
            'custom_field_3': '(ccc)(ST)(90210)',
            'custom_field_4': '(OOO)',
            'custom_field_5': '(Bob)(Patty)(family@example.com)',
            'custom_field_6': '(Memory)(no)(Good Jorb)',
            'custom_field_7': '(111 Somewhere)'
        })
        self.assertEqual(generate_custom_fields({}), {
            'custom_field_1': '()()',
            'custom_field_2': '()',
            'custom_field_3': '()()()',
            'custom_field_4': '()',
            'custom_field_5': '()()()',
            'custom_field_6': '(Honor)(yes)()',
            'custom_field_7': '()'
        })

    def test_humanize_amount(self):
        """ The humanize_amount function converts an amount in cents into
        something that's human readable. """
        self.assertEqual(humanize_amount(1520), '$15.20')
        self.assertEqual(humanize_amount(0), '$0.00')
