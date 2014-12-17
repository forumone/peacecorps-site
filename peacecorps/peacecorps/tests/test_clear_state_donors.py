from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from peacecorps.management.commands import clear_stale_donors as clear
from peacecorps.models import Account, DonorInfo


class ClearStaleDonorTests(TestCase):
    def test_handle(self):
        """Verify that expired donorinfo objects get deleted and that the
        appropriate logging message is made"""
        account = Account.objects.create(name='Example', code='EXEXEX')
        # Create several in the soon-to-be-past
        for i in range(5):
            DonorInfo.objects.create(
                agency_tracking_id=str(i)*5, account=account,
                expires_at=timezone.now())
        # Create one in the future
        DonorInfo.objects.create(
            agency_tracking_id='future', account=account,
            expires_at=timezone.now() + timedelta(hours=1))
        with self.assertLogs('peacecorps.clear_stale_donors') as logger:
            clear.Command().handle()
        self.assertEqual(1, account.donorinfos.count())
        self.assertEqual(1, len(logger.output))
        self.assertTrue('Deleted 5' in logger.output[0])
