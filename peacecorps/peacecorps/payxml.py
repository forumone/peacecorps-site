from xml.etree.ElementTree import Element, SubElement, Comment, tostring


def add_subelements(parent, data, elements):
    for element in elements:
        SubElement(parent, element, {'value': data[element]})
    return parent


def generate_collection_request(data):
    """ Generate the collection_request XML required by Pay.gov. """

    root = Element('collection_request')
    SubElement(root, 'protocol_version', {'value': '3.2'})
    SubElement(root, 'response_message', {'value': 'Success'})
    SubElement(root, 'action', {'value': 'SubmitCollectionInteractive'})

    interactive = SubElement(root, 'interactive_request')
    SubElement(interactive, 'allow_account_data_change', {'value':'True'})

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
    print(tostring(root))
    return root
