from django.core.urlresolvers import reverse
from django.test import TestCase

from peacecorps.models import DonorInfo, Account


class DataTests(TestCase):
    """Tests the data() view"""
    def setUp(self):
        self.account = Account.objects.create(code='FUNDFUND')
        self.donorinfo = DonorInfo.objects.create(
            agency_tracking_id='TRACK', account=self.account, xml='XML')

    def tearDown(self):
        self.account.delete()  # cascades

    def test_requires_post(self):
        result = self.client.get(reverse('paygov:data'),
                                 data={'agency_tracking_id': 'TRACK'})
        self.assertEqual(result.status_code, 405)

    def test_param(self):
        """The view requires a tracking id be present *and* valid"""
        result = self.client.post(reverse('paygov:data'))
        self.assertEqual(result.status_code, 400)

        result = self.client.post(reverse('paygov:data'),
                                  data={'agency_tracking_id': 'BAD'})
        self.assertEqual(result.status_code, 404)

    def test_success(self):
        result = self.client.post(reverse('paygov:data'),
                                  data={'agency_tracking_id': 'TRACK'})
        self.assertEqual(result.content, b'XML')
        self.assertEqual(result['Content-Type'], 'text/xml')


class ResultsTests(TestCase):
    """Tests the results() view"""
    def setUp(self):
        self.account = Account.objects.create(code='FUNDFUND')
        self.donorinfo = DonorInfo.objects.create(
            agency_tracking_id='TRACK', account=self.account, xml='XML')

    def tearDown(self):
        self.account.delete()  # cascades

    def test_requires_post(self):
        result = self.client.get(reverse('paygov:results'),
                                 data={'agency_tracking_id': 'TRACK'})
        self.assertEqual(result.status_code, 405)

    def test_param(self):
        """The view requires several fields and specific formats for those
        fields."""
        successful = {'agency_tracking_id': 'TRACK',
                      'payment_status': 'Completed',
                      'payment_amount': '125.00'}
        data = dict(successful)
        del data['agency_tracking_id']
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'agency_tracking_id')

        data = dict(successful, agency_tracking_id='BAD')
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'agency_tracking_id')

        data = dict(successful, payment_status='Canceled')
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'Unknown error')

        data['error_message'] = 'ABCDEFG'
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'ABCDEFG')

        data = dict(successful)
        del data['payment_amount']
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'payment_amount')

        data = dict(successful, payment_amount='1.2.3')
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'payment_amount')

    def test_success(self):
        """Verify mimetype and that donation is made when passed the right
        values"""
        successful = {'agency_tracking_id': 'TRACK',
                      'payment_status': 'Completed',
                      'payment_amount': '125.00'}
        result = self.client.post(reverse('paygov:results'), data=successful)
        self.assertEqual(result.content, b'response_message=OK')
        self.assertEqual(result['Content-Type'], 'text/plain')

        # avoiding the cache
        account = Account.objects.get(pk=self.account.pk)
        self.assertEqual(1, len(account.donations.all()))
        donation = account.donations.all()[0]
        self.assertEqual(donation.amount, 12500)
        self.assertEqual(0, len(account.donorinfos.all()))
