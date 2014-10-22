from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from uuid import uuid4

from django.conf import settings

from peacecorps.models import DonorInfo, humanize_amount


def add_subelements(parent, data, elements):
    for element in elements:
        SubElement(parent, element, {'value': str(data[element])})
    return parent


def generate_agency_memo(data):
    """Build the memo field from selections on the form"""
    memo = ''
    memo += '(' + data.get('comments', '').strip() + ')'
    memo += '(' + data.get('phone_number', '').strip() + ')'

    amount = humanize_amount(data['payment_amount'])
    memo += '(%s, %s)' % (data['project_code'], amount)

    if data.get('information_consent', '') == 'vol-consent-yes':
        memo += '(yes)'
    else:
        memo += '(no)'

    if data.get('interest_conflict'):
        memo += '(yes)'
    else:
        memo += '(no)'

    if data.get('email_consent'):
        memo += '(yes)'
    else:
        memo += '(no)'

    return memo


def generate_agency_tracking_id():
    """ Generate an agency tracking ID for the transaction that has some random
    component. I include the date in here too, in case that's useful. (The
    current non-random tracking id has the date in it.)
    @todo - make this more random"""

    random = str(uuid4()).replace('-', '')
    today = datetime.now().strftime("%m%d")
    return 'PCOCI%s%s' % (today, random[0:6])


def generate_collection_request(data):
    """ Generate the collection_request XML required by Pay.gov. """

    root = Element('collection_request')
    SubElement(root, 'protocol_version', {'value': '3.2'})
    SubElement(root, 'response_message', {'value': 'Success'})
    SubElement(root, 'action', {'value': 'SubmitCollectionInteractive'})

    interactive = SubElement(root, 'interactive_request')
    SubElement(interactive, 'allow_account_data_change', {'value': 'True'})

    collection_auth = SubElement(interactive, 'collection_auth')
    collection_fields = [
        'agency_tracking_id', 'agency_memo', 'form_id', 'payment_amount']
    add_subelements(collection_auth, data, collection_fields)

    account_data = SubElement(collection_auth, 'account_data')
    account_fields = [
        'payment_type', 'payer_name', 'billing_address', 'billing_city',
        'billing_state', 'billing_zip']
    add_subelements(account_data, data, account_fields)

    optional_fields = SubElement(collection_auth, 'OptionalFieldsGroup')
    custom_fields = [
        'custom_field_1', 'custom_field_2', 'custom_field_3', 'custom_field_4',
        'custom_field_5', 'custom_field_6', 'custom_field_7']
    add_subelements(optional_fields, data, custom_fields)
    return root


def generate_custom_fields(data):
    """Return a dictionary composed of 'custom' fields, formatted the way we
    expect."""
    custom = {}
    custom['custom_field_1'] = '(' + data.get('phone_number', '') + ')'
    custom['custom_field_1'] += '(' + data.get('email', '') + ')'
    custom['custom_field_2'] = '(' + data.get('billing_address', '') + ')'

    custom['custom_field_3'] = '(' + data.get('billing_city', '') + ')'
    custom['custom_field_3'] += '(' + data.get('billing_state', '') + ')'
    custom['custom_field_3'] += '(' + data.get('billing_zip', '') + ')'
    custom['custom_field_4'] = '(' + data.get('organization_name', '') + ')'

    custom['custom_field_5'] = '(' + data.get('dedication_name', '') + ')'
    custom['custom_field_5'] += '(' + data.get('dedication_contact', '') + ')'
    custom['custom_field_5'] += '(' + data.get('dedication_email', '') + ')'

    if data.get('dedication_type') == 'in-memory':
        custom['custom_field_6'] = '(Memory)'
    else:
        custom['custom_field_6'] = '(Honor)'
    if data.get('dedication_consent') == 'no-dedication-consent':
        custom['custom_field_6'] += '(no)'
    else:
        custom['custom_field_6'] += '(yes)'
    custom['custom_field_6'] += '(' + data.get('card_dedication', '') + ')'
    custom['custom_field_7'] = '(' + data.get('dedication_address', '') + ')'
    return custom


def convert_to_paygov(data, fund):
    """Convert the form data into a pay.gov model (including appropriate XML)
    and return."""
    data = dict(data)   # shallow copy
    tracking_id = generate_agency_tracking_id()
    data['agency_tracking_id'] = tracking_id
    data['agency_memo'] = generate_agency_memo(data)
    data['form_id'] = settings.PAY_GOV_FORM_ID
    data.update(generate_custom_fields(data))
    xml = generate_collection_request(data)
    return DonorInfo(agency_tracking_id=tracking_id, fund=fund,
                     xml=tostring(xml))
