from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from urllib.parse import urlencode
from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse

from peacecorps.models import Account, DonorInfo
from peacecorps.templatetags.humanize_cents import humanize_cents


def add_subelements(parent, data, elements):
    for element in elements:
        SubElement(parent, element, {'value': str(data[element])})
    return parent


def generate_agency_memo(data):
    """Build the memo field from selections on the form. Format should be
        (Donor Comment)(Project Number, Amount)(Donor Phone Number)
        (Contact info consent)(Bus Interest Conflict)(Contact Email Consent).
    """
    memo = ''
    memo += '(' + data.get('comments', '').strip() + ')'

    amount = humanize_cents(data['payment_amount'], commas=False)
    memo += '(%s,%s/)' % (data['project_code'], amount)

    memo += '(' + data.get('phone_number', '').strip() + ')'

    if data.get('information_consent'):
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
    SubElement(interactive, 'success_return_url',
               {'value': data['success_url']})
    SubElement(interactive, 'failure_return_url',
               {'value': data['failure_url']})
    SubElement(interactive, 'allow_account_data_change', {'value': 'True'})

    collection_auth = SubElement(interactive, 'collection_auth')
    collection_fields = ['agency_tracking_id', 'agency_memo', 'form_id']
    add_subelements(collection_auth, data, collection_fields)
    SubElement(collection_auth, 'payment_amount',
               {'value': "%.2f" % (data['payment_amount'] / 100.0)})

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
    expect. Format is
        Custom Field #1: Phone_Number,Email_Address
        Custom Field #2: Address
        Custom Field #3: City, State, Zip
        Custom Field #4: Organization_Name
        Custom Field #5: Dedication_Name, Contact, Email
        Custom Field #6: Dedication_Type, Consent, Message
        Custom Field #7: Dedication_Address"""
    custom = {}
    custom['custom_field_1'] = '(' + data.get('phone_number', '') + ')'
    custom['custom_field_1'] += '(' + data.get('email', '') + ')'

    custom['custom_field_2'] = '(' + data.get('billing_address', '') + ')'

    custom['custom_field_3'] = '(' + data.get('billing_city', '') + ')'
    custom['custom_field_3'] += '(' + data.get('billing_state', '') + ')'
    custom['custom_field_3'] += '(' + data.get('billing_zip', '') + ')'

    custom['custom_field_4'] = '(' + data.get('organization_contact', '') + ')'

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


def redirect_urls(account, donor_name):
    """Success and return URLs are derived from the account. Also the
    donor's first name to the url"""
    if account.category == Account.PROJECT:
        project = account.project_set.first()
        return (reverse('project success', kwargs={'slug': project.slug})
                + '?' + urlencode({'donor_name': donor_name}),
                reverse('project failure', kwargs={'slug': project.slug}))
    else:
        campaign = account.campaign_set.first()
        return (reverse('campaign success', kwargs={'slug': campaign.slug})
                + '?' + urlencode({'donor_name': donor_name}),
                reverse('campaign failure', kwargs={'slug': campaign.slug}))


def convert_to_paygov(data, account, callback_base):
    """Convert the form data into a pay.gov model (including appropriate XML)
    and return."""
    data = dict(data)   # shallow copy
    tracking_id = generate_agency_tracking_id()
    data['agency_tracking_id'] = tracking_id
    data['agency_memo'] = generate_agency_memo(data)
    data['form_id'] = settings.PAY_GOV_FORM_ID
    # quick method of finding the donor's first name
    donor_first = data.get('payer_name', '').split(' ')[0]
    # payer_name could be the individual or organization field
    data['payer_name'] = data.get('payer_name',
                                  data.get('organization_name', ''))
    data['success_url'], data['failure_url'] = (
        callback_base + url for url in redirect_urls(account, donor_first))
    data.update(generate_custom_fields(data))
    xml = generate_collection_request(data)
    return DonorInfo(agency_tracking_id=tracking_id, account=account,
                     xml=tostring(xml).decode('utf-8'))
