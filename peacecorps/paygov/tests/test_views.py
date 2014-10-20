from django.core.urlresolvers import reverse
from django.test import TestCase

from paygov.models import DonorInfo
from peacecorps.models import Fund


class DataTests(TestCase):
    """Tests the data() view"""
    def setUp(self):
        self.fund = Fund.objects.create(fundcode='FUNDFUND')
        self.donorinfo = DonorInfo.objects.create(agency_tracking_id='TRACK',
                                                  fund=self.fund, xml='XML')

    def tearDown(self):
        self.fund.delete()  # cascades

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
        self.assertEqual(result.status_code, 400)

    def test_success(self):
        result = self.client.post(reverse('paygov:data'),
                                  data={'agency_tracking_id': 'TRACK'})
        self.assertEqual(result.content, b'XML')
