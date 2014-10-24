import os.path
import shutil
from unittest import skipUnless

from django.test import TestCase

from peacecorps.models import DonorInfo, Fund


class GPGTests(TestCase):
    def setUp(self):
        self.fund = Fund.objects.create(fundcode='FUNDFUND')

    def tearDown(self):
        self.fund.delete()

    def test_no_encryption(self):
        """With no encryption settings, fields still work"""
        with self.settings(GNUPG_HOME=''):
            di = DonorInfo(agency_tracking_id='TRACK', fund=self.fund,
                           xml='Plain Text')
            di.save()

            #   Was saved in plain text in the DB
            values = DonorInfo.objects.filter(pk=di.pk).values_list('xml')
            byte_str = values[0][0]
            self.assertEqual(byte_str.decode('utf-8'), 'Plain Text')

            #   Decodes correctly
            from_db = DonorInfo.objects.get(pk=di.pk)
            self.assertEqual(from_db.xml, 'Plain Text')

    @skipUnless(shutil.which('gpg'), "GPG is not installed")
    def test_encryption(self):
        """Verify that fields *are* encrypted when GNUPG_HOME is set"""
        with self.settings(GNUPG_HOME=os.path.join('peacecorps', 'tests',
                                                   'gpg'),
                           GPG_RECIPIENTS={
                               'peacecorps.fields.GPGField.xml': 'C68F6B22'}):
            di = DonorInfo(agency_tracking_id='TRACK', fund=self.fund,
                           xml='Plain Text')
            di.save()

            #   Was *not* saved in plain text in the DB
            values = DonorInfo.objects.filter(pk=di.pk).values_list('xml')
            byte_str = values[0][0]
            self.assertTrue('BEGIN PGP' in byte_str.decode('utf-8'))

            #   Decodes correctly
            from_db = DonorInfo.objects.get(pk=di.pk)
            self.assertEqual(from_db.xml, 'Plain Text')
