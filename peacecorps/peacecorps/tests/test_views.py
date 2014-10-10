from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.utils.importlib import import_module

from peacecorps.views import generate_agency_tracking_id, generate_agency_memo
from peacecorps.views import generate_custom_fields, humanize_amount
from peacecorps.payxml import generate_collection_request

from xml.etree.ElementTree import tostring

def donor_custom_fields():
    data = {'phone_number': '1112223333', 'email': 'aaa@example.com',
            'street_address': 'stttt', 'city': 'ccc', 'state': 'ST',
            'zip_code': '90210', 'organization_name': 'OOO',
            'dedication_name': 'Bob', 'dedication_contact': 'Patty',
            'dedication_email': 'family@example.com',
            'dedication_type': 'in-memory',
            'dedication_consent': 'no-dedication-consent',
            'card_dedication': 'Good Jorb',
            'dedication_address': '111 Somewhere'}
    return data

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
            '/donations/contribute/?amount=2000&project=14-532-001')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('$20.00' in content)
        self.assertTrue('14-532-001')

    def test_review_page(self):
        """ Test that the donation review page renders with the required
        elements. """

        form_data = {
            'name': 'William Williams',
            'street_address':  '1 Main Street',
            'city': 'Anytown',
            'state': 'MD',
            'zip_code':  '20852',
            'country': 'USA',
            'donation_amount': 2000,
            'project_code': 'PC-SEC01',
            'donor_type': 'Individual',
            'payment_type': 'credit-card',
            'information_consent': 'vol-consent-yes'}

        response = self.client.post(
            '/donations/contribute/?amount=2000&project=14-532-001', form_data)
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        memo = generate_agency_memo(form_data)
        self.assertTrue(memo in content)
        self.assertTrue('agency_tracking_id' in content)
        self.assertTrue('agency_id' in content)

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
        data = donor_custom_fields()

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

    def test_bad_request_donations(self):
        """ The donation information page should 400 if donation amount and
        project code aren't included. """
        response = self.client.get('/donations/contribute')
        self.assertEqual(response.status_code, 400)

    def test_bad_amount(self):
        """ If a non-integer amount is entered, the donations/contribute page
        should 400. """

        response = self.client.get(
            '/donations/contribute/?amount=aaa&project_code=154')
        self.assertEqual(response.status_code, 400)


class DonatePagesTests(TestCase):

    fixtures = ['tests.yaml']

    def setUp(self):
        self.client = Client()

    # Do the pages load without error?
    def test_pages_rendering(self):
        response = self.client.get('/donate')
        self.assertEqual(response.status_code, 200)

    def test_issue_rendering(self):
        response = self.client.get('/donate/issue/innovation')
        self.assertEqual(response.status_code, 200)

    def test_project_rendering(self):
        response = self.client.get('/donate/project/test-project')
        self.assertEqual(response.status_code, 200)


class PayXMLGenerationTests(TestCase):
    def test_xml(self):
        data = {
            'agency_tracking_id': 'PCIOCI1234',
            'agency_memo': '()(5555555)',
            'form_id': 'DONORFORM',
            'donation_amount': '20.00',
            'payment_type': 'CreditCard',
            'name': 'William Williams',
            'street_address': '1 Main St',
            'city': 'Anytown', 
            'state': 'MD', 
            'zip_code': '20852'
        }

        data.update(generate_custom_fields(donor_custom_fields()))
        
        collection_request = generate_collection_request(data)
        self.assertEqual('collection_request', collection_request.tag)
        protocol_versions = collection_request.findall('.//protocol_version')
        self.assertEqual(len(protocol_versions), 1)
        response_message = collection_request.findall('.//response_message')[0]
        self.assertEqual(response_message.attrib['value'], 'Success')
        action = collection_request.findall('.//action')[0]
        self.assertEqual(action.attrib['value'], 'SubmitCollectionInteractive')
