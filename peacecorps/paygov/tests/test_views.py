import logging

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

        data = dict(successful)
        del data['payment_amount']
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'payment_amount')

        data = dict(successful, payment_amount='1.2.3')
        result = self.client.post(reverse('paygov:results'), data=data)
        self.assertContains(result, 'payment_amount')

    def test_cancelation(self):
        """If we receive notification that the payment was not a success,
        delete the associated donorinfo and log accordingly"""
        data = {'agency_tracking_id': 'TRACK', 'payment_status': 'Canceled',
                'payment_amount': '125.00', 'error_message': 'ABCDEFG'}
        with self.assertLogs('paygov.results', level=logging.WARN) as logger:
            result = self.client.post(reverse('paygov:results'), data=data)
            self.assertContains(result, 'ABCDEFG')
        self.assertEqual(
            0, DonorInfo.objects.filter(agency_tracking_id='TRACK').count())
        self.assertEqual(1, len(logger.output))
        self.assertTrue('Canceled' in logger.output[0])
        self.assertTrue('ABCDEFG' in logger.output[0])

    def test_success(self):
        """Verify mimetype and that donation is made when passed the right
        values. A message should also be logged"""
        successful = {'agency_tracking_id': 'TRACK',
                      'payment_status': 'Completed',
                      'payment_amount': '125.00'}
        with self.assertLogs('paygov.results') as logger:
            result = self.client.post(reverse('paygov:results'),
                                      data=successful)
            self.assertEqual(result.content, b'response_message=OK')
            self.assertEqual(result['Content-Type'], 'text/plain')
        self.assertEqual(1, len(logger.output))
        self.assertTrue('Transaction success' in logger.output[0])
        self.assertTrue('12500 cents' in logger.output[0])
        self.assertTrue('FUNDFUND' in logger.output[0])

        # avoiding the cache to verify the donor info's been deleted
        account = Account.objects.get(pk=self.account.pk)
        self.assertEqual(1, len(account.donations.all()))
        donation = account.donations.all()[0]
        self.assertEqual(donation.amount, 12500)
        self.assertEqual(0, len(account.donorinfos.all()))

    def test_other_amount_formats(self):
        """The payment_amount format returned by pay.gov varies"""
        self.donorinfo.delete()     # we'll make a few in the loop
        for amount in ('125', '125.0', '125.', '125.00'):
            self.donorinfo = DonorInfo.objects.create(
                agency_tracking_id='TRACK', account=self.account, xml='XML')
            successful = {'agency_tracking_id': 'TRACK',
                          'payment_status': 'Completed',
                          'payment_amount': amount}
            result = self.client.post(reverse('paygov:results'),
                                      data=successful)
            self.assertEqual(result.content, b'response_message=OK')

            # avoiding the cache
            account = Account.objects.get(pk=self.account.pk)
            donation = account.donations.order_by('-pk')[0]
            self.assertEqual(donation.amount, 12500)
