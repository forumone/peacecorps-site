from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def generate_collection_request(data):
    """ Generate the collection_request XML required by Pay.gov. """

    root = Element('collection_request')
    SubElement(root, 'protocol_version', {'value': '3.2'})
    SubElement(root, 'response_message', {'value': 'Success'})
    SubElement(root, 'action', {'value': 'SubmitCollectionInteractive'})

    interactive = SubElement(root, 'interactive_request')
    SubElement(interactive, 'allow_account_data_change', {'value':'True'})

    collection_auth = SubElement(interactive, 'collection_auth')
    SubElement(
        collection_auth, 'agency_tracking_id',
        {'value': data['agency_tracking_id']})
    SubElement(collection_auth, 'agency_memo', {'value': data['agency_memo']})
    SubElement(collection_auth, 'form_id', {'value': data['form_id']})
    SubElement(
        collection_auth, 'payment_amount', {'value': data['donation_amount']})

    account_data = SubElement(collection_auth, 'account_data') 
    SubElement(account_data, 'payment_type', {'value': data['payment_type']})
    SubElement(account_data, 'payer_name', {'value': data['name']})
    SubElement(
        account_data, 'billing_address', {'value': data['billing_address']})
    SubElement(account_data, 'billing_city', {'value': data['city']})
    SubElement(account_data, 'billing_state', {'value': data['state']})
    SubElement(account_data, 'billing_zip', {'value': data['zip_code']})

    optional_fields = SubElement(collection_auth, 'OptionalFieldsGroup')
    SubElement(optional_fields, 'custom_field_1', {'value': data['custom_field_1']})
    SubElement(optional_fields, 'custom_field_2', {'value': data['custom_field_2']})
    SubElement(optional_fields, 'custom_field_3', {'value': data['custom_field_3']})
    SubElement(optional_fields, 'custom_field_4', {'value': data['custom_field_4']})
    SubElement(optional_fields, 'custom_field_5', {'value': data['custom_field_5']})
    SubElement(optional_fields, 'custom_field_6', {'value': data['custom_field_6']})
    SubElement(optional_fields, 'custom_field_7', {'value': data['custom_field_7']})

    print(tostring(root))
    return root
