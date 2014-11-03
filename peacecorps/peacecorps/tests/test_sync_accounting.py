from datetime import datetime
import tempfile

from django.test import TestCase
from django.utils import timezone

from peacecorps.management.commands.sync_accounting import cents_from, Command
from peacecorps.management.commands.sync_accounting import datetime_from
from peacecorps.models import Donation, Account


class SyncAccountingTests(TestCase):
    def test_datetime_from(self):
        dt = datetime_from('2012-03-20 16:45:01')
        self.assertEqual(2012, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(20, dt.day)
        self.assertEqual(16, dt.hour)
        self.assertEqual(45, dt.minute)
        self.assertEqual(1, dt.second)

    def test_cents_from(self):
        self.assertEqual(123456789, cents_from('1,234,567.89'))
        self.assertEqual(12300, cents_from('123'))
        self.assertRaises(ValueError, cents_from, '12.34.56')

    def test_command(self):
        """Use fake data to verify that amount fields are updated and old
        transactions are deleted"""
        filedata = "PROJ_NO,OTHER_FIELD,LAST_UPDATED_FROM_PAYGOV,REVENUE\n"
        filedata += '123-456,Some Content,2009-12-14 15:16:17,"1,234"\n'
        filedata += "nonexist,Not Here,2009-12-14 15:16:17,1.23\n"
        filedata += "111-222,Other Content,2009-12-14 15:16:17,1.23\n"
        csv_file_handle, csv_path = tempfile.mkstemp()
        with open(csv_file_handle, 'w') as csv_file:
            csv_file.write(filedata)

        account456 = Account.objects.create(name='account1', code='123-456')
        account222 = Account.objects.create(name='account2', code='111-222')
        tz = timezone.get_current_timezone()
        before_donation = Donation.objects.create(
            account=account222, amount=5432)
        before_donation.time = timezone.make_aware(
            datetime(2009, 12, 14, 15, 16), tz)
        before_donation.save()
        after_donation = Donation.objects.create(
            account=account222, amount=5432)
        after_donation.time = timezone.make_aware(
            datetime(2009, 12, 14, 16), tz)
        after_donation.save()

        command = Command()
        command.handle(csv_path)

        # before_donation should be deleted, but after_donation not
        self.assertEqual(
            None, Donation.objects.filter(pk=before_donation.pk).first())
        self.assertNotEqual(
            None, Donation.objects.filter(pk=after_donation.pk).first())

        # amount donated to each should also be updated
        self.assertEqual(123400, Account.objects.get(pk=account456.pk).current)
        self.assertEqual(123, Account.objects.get(pk=account222.pk).current)
