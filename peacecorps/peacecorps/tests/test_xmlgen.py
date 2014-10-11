from django.test import TestCase

from peacecorps.views import generate_custom_fields
from peacecorps.payxml import generate_collection_request
from .test_views import donor_custom_fields
from xml.etree.ElementTree import tostring

class PayXMLGenerationTests(TestCase):
    def test_xml(self):
        data = {
            'agency_tracking_id': 'PCIOCI1234',
            'agency_memo': '()(5555555)',
            'form_id': 'DONORFORM',
            'payment_amount': '20.00',
            'payment_type': 'CreditCard',
            'payer_name': 'William Williams',
            'billing_address': '1 Main St',
            'billing_city': 'Anytown', 
            'billing_state': 'MD', 
            'billing_zip': '20852'
        }

        data.update(generate_custom_fields(donor_custom_fields()))
        
        collection_request = generate_collection_request(data)
        self.assertEqual('collection_request', collection_request.tag)
        protocol_versions = collection_request.findall('./protocol_version')
        self.assertEqual(len(protocol_versions), 1)

        response_message = collection_request.findall('.//response_message')[0]
        self.assertEqual(response_message.attrib['value'], 'Success')

        action = collection_request.findall('.//action')[0]
        self.assertEqual(action.attrib['value'], 'SubmitCollectionInteractive')

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
        optg += '<custom_field_4 value="(OOO)" />'
        optg += '<custom_field_5 value="(Bob)(Patty)(family@example.com)" />'
        optg += '<custom_field_6 value="(Memory)(no)(Good Jorb)" />'
        optg += '<custom_field_7 value="(111 Somewhere)" />'
        optg += '</OptionalFieldsGroup>'

        self.assertEqual(optg, tostring(optional_fields).decode('utf-8'))


