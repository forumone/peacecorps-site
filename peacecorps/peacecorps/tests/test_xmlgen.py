from xml.etree.ElementTree import tostring

from django.test import TestCase

from peacecorps import payxml
from peacecorps.models import Account, Country, Campaign, Project


def donor_custom_fields():
    data = {'phone_number': '1112223333', 'email': 'aaa@example.com',
            'billing_address': 'stttt', 'billing_city': 'ccc',
            'billing_state': 'ST',
            'billing_zip': '90210', 'organization_contact': 'Bob Jones',
            'dedication_name': 'Bob', 'dedication_contact': 'Patty',
            'dedication_email': 'family@example.com',
            'dedication_type': 'in-memory',
            'dedication_consent': 'no-dedication-consent',
            'card_dedication': 'Good Jorb',
            'dedication_address': '111 Somewhere'}
    return data


class PayXMLGenerationTests(TestCase):
    fixtures = ['countries.yaml']

    def test_xml(self):
        data = {
            'agency_tracking_id': 'PCIOCI1234',
            'agency_memo': '()(5555555)',
            'form_id': 'DONORFORM',
            'payment_amount': 2000,
            'payment_type': 'CreditCard',
            'payer_name': 'William Williams',
            'billing_address': '1 Main St',
            'billing_city': 'Anytown',
            'billing_state': 'MD',
            'billing_zip': '20852',
            'success_url': 'https://success.com',
            'failure_url': 'https://failure.com'
        }

        data.update(payxml.generate_custom_fields(donor_custom_fields()))

        collection_request = payxml.generate_collection_request(data)
        self.assertEqual('collection_request', collection_request.tag)
        protocol_versions = collection_request.findall('./protocol_version')
        self.assertEqual(len(protocol_versions), 1)

        response_message = collection_request.findall('.//response_message')[0]
        self.assertEqual(response_message.attrib['value'], 'Success')

        action = collection_request.findall('.//action')[0]
        self.assertEqual(action.attrib['value'], 'SubmitCollectionInteractive')

        success_el = collection_request.findall(
            './interactive_request/success_return_url')[0]
        self.assertEqual(success_el.attrib['value'], 'https://success.com')
        failure_el = collection_request.findall(
            './interactive_request/failure_return_url')[0]
        self.assertEqual(failure_el.attrib['value'], 'https://failure.com')

        account_data = collection_request.findall(
            './interactive_request/collection_auth/account_data')[0]
        account_xml = '<account_data><payment_type value="CreditCard" />'
        account_xml += '<payer_name value="William Williams" />'
        account_xml += '<billing_address value="1 Main St" />'
        account_xml += '<billing_city value="Anytown" />'
        account_xml += '<billing_state value="MD" />'
        account_xml += '<billing_zip value="20852" /></account_data>'

        self.assertEqual(account_xml, tostring(account_data).decode('utf-8'))

        payment_amount = collection_request.findall(
            './interactive_request/collection_auth/payment_amount')[0]
        self.assertEqual(payment_amount.attrib['value'], '20.00')

        optional_fields = collection_request.findall(
            './interactive_request/collection_auth/OptionalFieldsGroup')[0]

        optg = '<OptionalFieldsGroup>'
        optg += '<custom_field_1 value="(1112223333)(aaa@example.com)" />'
        optg += '<custom_field_2 value="(stttt)" />'
        optg += '<custom_field_3 value="(ccc)(ST)(90210)" />'
        optg += '<custom_field_4 value="(Bob Jones)" />'
        optg += '<custom_field_5 value="(Bob)(Patty)(family@example.com)" />'
        optg += '<custom_field_6 value="(Memory)(no)(Good Jorb)" />'
        optg += '<custom_field_7 value="(111 Somewhere)" />'
        optg += '</OptionalFieldsGroup>'

        self.assertEqual(optg, tostring(optional_fields).decode('utf-8'))

    def test_generate_agency_memo(self):
        """The data dictionary should be serialized in the predictable way.
        Allow all fields to be optional"""
        data = {'comments': 'CCCCCC', 'phone_number': '5555555555',
                'information_consent': True,
                'payment_amount': 2000, 'project_code': '14-54FF',
                'interest_conflict': True, 'email_consent': True}
        memo = payxml.generate_agency_memo(data)
        self.assertEqual(
            "(CCCCCC)(14-54FF,$20.00/)(5555555555)(yes)(yes)(yes)", memo)

        memo = payxml.generate_agency_memo({
            'payment_amount': 2000, 'project_code': '14-54FF'})
        self.assertEqual("()(14-54FF,$20.00/)()(no)(no)(no)", memo)

        memo = payxml.generate_agency_memo({
            'comments': 'This is a good project.',
            'project_code': '15-680-008',
            'payment_amount': 4000,
            'phone_number': '1234567890',
            'information_consent': True, 'interest_conflict': False,
            'email_consent': False})
        self.assertEqual(
            "(This is a good project.)(15-680-008,$40.00/)(1234567890)"
            "(yes)(no)(no)",
            memo)

        # No commas should be present in the amount
        memo = payxml.generate_agency_memo({
            'payment_amount': 1234567, 'project_code': '14-54FF'})
        self.assertEqual("()(14-54FF,$12345.67/)()(no)(no)(no)", memo)

        # New lines and other special characters get removed
        memo = payxml.generate_agency_memo({
            'comments': 'This\nHas\tSome\aSpecial\rChars\b',
            'payment_amount': 1245, 'project_code': '111-222'})
        self.assertEqual("(This Has Some Special Chars)(111-222,$12.45/)"
                         "()(no)(no)(no)", memo)

    def test_generate_custom_fields(self):
        """The data dictionary should be serialized in the predictable way."""
        data = donor_custom_fields()
        self.assertEqual(payxml.generate_custom_fields(data), {
            'custom_field_1': '(1112223333)(aaa@example.com)',
            'custom_field_2': '(stttt)',
            'custom_field_3': '(ccc)(ST)(90210)',
            'custom_field_4': '(Bob Jones)',
            'custom_field_5': '(Bob)(Patty)(family@example.com)',
            'custom_field_6': '(Memory)(no)(Good Jorb)',
            'custom_field_7': '(111 Somewhere)'
        })

    def test_generate_custom_fields_optional(self):
        """Allow all fields to be optional"""
        self.assertEqual(payxml.generate_custom_fields({}), {
            'custom_field_1': '()()',
            'custom_field_2': '()',
            'custom_field_3': '()()()',
            'custom_field_4': '()',
            'custom_field_5': '()()()',
            'custom_field_6': '(Honor)(yes)()',
            'custom_field_7': '()'
        })

    def test_generate_custom_fields_escape_chars(self):
        """Handle escaped chars in dedication"""
        data = {'card_dedication': "Here\nis\rAn\aalert"}
        self.assertEqual(payxml.generate_custom_fields(data), {
            'custom_field_1': '()()',
            'custom_field_2': '()',
            'custom_field_3': '()()()',
            'custom_field_4': '()',
            'custom_field_5': '()()()',
            'custom_field_6': '(Honor)(yes)(Here is An alert)',
            'custom_field_7': '()'
        })

    def test_generate_agency_tracking_id(self):
        """ This just tests the start of a generated tracking id, which is
        currently the only piece we're sure of. """

        tracking_id = payxml.generate_agency_tracking_id()
        self.assertTrue(tracking_id.startswith('PCOCI'))

    def test_redirect_urls(self):
        account = Account.objects.create(category=Account.PROJECT)
        proj = Project.objects.create(
            account=account, country=Country.objects.get(name='Canada'),
            slug='proj-proj')
        campaign = Campaign.objects.create(
            account=account, slug='cccccc')

        succ, fail = payxml.redirect_urls(account)
        self.assertTrue('success' in succ)
        self.assertTrue('project' in succ)
        self.assertTrue('failure' in fail)
        self.assertTrue('project' in fail)
        proj.delete()

        account.category = Account.COUNTRY
        succ, fail = payxml.redirect_urls(account)
        self.assertTrue('success' in succ)
        self.assertTrue('fund' in succ)
        self.assertTrue('failure' in fail)
        self.assertTrue('fund' in fail)

        campaign.delete()
        account.delete()

    def test_convert_to_paygov_organization(self):
        """Organization donors should also have all data present"""
        data = donor_custom_fields()
        data['organization_contact'] = 'Bob Smith'
        data['organization_name'] = 'ABC Corp'
        data['payment_amount'] = 1234
        data['project_code'] = '111-222'
        data['payment_type'] = 'CreditCard'
        account = Account.objects.create(code='111-222',
                                         category=Account.PROJECT)
        Project.objects.create(
            account=account, country=Country.objects.get(name='Canada'),
            slug='proj-proj')

        result = payxml.convert_to_paygov(data, account, "http://example.com")
        xml = result.xml
        self.assertTrue('(Bob Smith)' in xml)
        self.assertTrue('ABC Corp' in xml)
        account.delete()
