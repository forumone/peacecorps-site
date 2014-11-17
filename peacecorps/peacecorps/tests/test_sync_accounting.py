from datetime import datetime
import tempfile
from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils import timezone

from peacecorps.management.commands import sync_accounting as sync
from peacecorps.models import (
    Account, Campaign, Donation, Project, SectorMapping)


class SyncAccountingTests(TestCase):
    fixtures = ['tests.yaml']

    def test_datetime_from(self):
        dt = sync.datetime_from('2012-03-20 16:45:01')
        self.assertEqual(2012, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(20, dt.day)
        self.assertEqual(16, dt.hour)
        self.assertEqual(45, dt.minute)
        self.assertEqual(1, dt.second)

        #   @todo remove this test once the data is cleaned up
        dt = sync.datetime_from('9-Oct-12')
        self.assertEqual(2012, dt.year)
        self.assertEqual(10, dt.month)
        self.assertEqual(9, dt.day)
        self.assertEqual(0, dt.hour)
        self.assertEqual(0, dt.minute)
        self.assertEqual(0, dt.second)

    def test_cents_from(self):
        self.assertEqual(123456789, sync.cents_from('1,234,567.89'))
        self.assertEqual(12300, sync.cents_from('123'))
        self.assertRaises(ValueError, sync.cents_from, '12.34.56')

    def test_update_account(self):
        """Use fake data to verify that amount fields are updated and old
        transactions are deleted"""
        acc222 = Account.objects.create(
            name='Account222', code='111-222', category=Account.PROJECT)

        tz = timezone.get_current_timezone()
        before_donation = Donation.objects.create(account=acc222, amount=5432)
        before_donation.time = timezone.make_aware(
            datetime(2009, 12, 14, 15, 16), tz)
        before_donation.save()
        after_donation = Donation.objects.create(account=acc222, amount=5432)
        after_donation.time = timezone.make_aware(
            datetime(2009, 12, 14, 16), tz)
        after_donation.save()

        # First test with an empty LAST_UPDATED value
        row = {'LAST_UPDATED_FROM_PAYGOV': '', 'PROJ_REQUEST': '444',
               'PROJ_BAL': '110.7'}
        sync.update_account(row, acc222)
        # All donations should remain
        self.assertNotEqual(
            None, Donation.objects.filter(pk=before_donation.pk).first())
        self.assertNotEqual(
            None, Donation.objects.filter(pk=after_donation.pk).first())
        # amount donated to should be updated
        self.assertEqual(33330, Account.objects.get(pk=acc222.pk).current)

        row = {'LAST_UPDATED_FROM_PAYGOV': '2009-12-14 15:16:17',
               'PROJ_REQUEST': '5,555.55', 'PROJ_BAL': '4,321.32'}
        sync.update_account(row, acc222)
        # before_donation should be deleted, but after_donation not
        self.assertEqual(
            None, Donation.objects.filter(pk=before_donation.pk).first())
        self.assertNotEqual(
            None, Donation.objects.filter(pk=after_donation.pk).first())

        # amount donated to should also be updated
        self.assertEqual(123423, Account.objects.get(pk=acc222.pk).current)

    def test_create_pcpp(self):
        """Use fake data to generate a new pcpp"""
        account = Account(name='New Project Effort', code='098-765',
                          category=Account.PROJECT)
        row = {
            'PROJ_CODE': '098-765', 'COUNTRY_NAME': 'CHINA',
            'PROJ_NAME': 'New Project Effort', 'PCV_NAME': 'IN Jones, B.',
            'STATE': 'IN', 'COMM_CONTRIB': '1234.56', 'PROJ_REQUEST': '3,434',
            'PROJ_BAL': '1,111', 'SECTOR': 'IT', 'SUMMARY': 'sum sum sum'}
        issue_cache = Mock()
        issue_cache.find.return_value = Campaign.objects.get(name='Technology')
        sync.create_pcpp(account, row, issue_cache)
        project = Project.objects.get(title='New Project Effort')
        self.assertEqual(project.account.code, '098-765')
        self.assertEqual(project.country.name, 'China')
        self.assertEqual(project.volunteername, 'Jones, B.')
        self.assertEqual(project.volunteerhomestate, 'IN')
        self.assertEqual(project.account.community_contribution, 123456)
        self.assertEqual(project.account.goal, 343400)
        self.assertEqual(project.account.current, (343400 - 111100))
        self.assertEqual(project.overflow.name, 'Information Technology')
        self.assertEqual(project.campaigns.all()[0].name, 'Technology')
        self.assertEqual(project.description, 'sum sum sum')
        self.assertEqual(project.slug, 'new-project-effort')
        self.assertFalse(project.published)
        project.delete()
        account.delete()

    def test_create_pcpp_empty(self):
        """Community contribution might be empty"""
        account = Account(name='New Project Effort', code='098-765',
                          category=Account.PROJECT)
        row = {
            'PROJ_CODE': '098-765', 'COUNTRY_NAME': 'CHINA',
            'PROJ_NAME': 'New Project Effort', 'PCV_NAME': 'IN Jones, B.',
            'STATE': 'IN', 'COMM_CONTRIB': '', 'PROJ_REQUEST': '3,434',
            'PROJ_BAL': '1,111', 'SECTOR': 'IT', 'SUMMARY': 'sum sum sum'}
        issue_cache = Mock()
        issue_cache.find.return_value = Campaign.objects.get(name='Technology')
        sync.create_pcpp(account, row, issue_cache)
        project = Project.objects.get(title='New Project Effort')
        self.assertEqual(project.account.community_contribution, 0)
        self.assertEqual(project.account.goal, 343400)
        self.assertEqual(project.account.current, (343400 - 111100))
        account.delete()    # cascades

    @patch('peacecorps.management.commands.sync_accounting.create_pcpp')
    def test_create_account_project(self, create):
        """Test that execution is deferred to the create_pcpp method"""
        row = {'PROJ_NAME': 'Some Proj', 'PROJ_CODE': '121-212',
               'SECTOR': 'IT'}
        sync.create_account(row, None)
        self.assertTrue(create.called)
        account, row, issue_map = create.call_args[0]
        self.assertEqual(account.name, 'Some Proj')
        self.assertEqual(account.code, '121-212')
        self.assertEqual(account.category, Account.PROJECT)
        self.assertIsNone(account.pk)

    def test_create_account_campaign(self):
        """Campaigns should be created"""
        row = {'PROJ_NAME': 'Argentina Fund', 'PROJ_CODE': '789-CFD',
               'SUMMARY': 'Some Sum'}
        sync.create_account(row, None)
        account = Account.objects.get(code='789-CFD')
        campaign = Campaign.objects.get(account=account)
        self.assertEqual(campaign.name, 'Argentina Fund')
        self.assertEqual(campaign.account, account)
        self.assertEqual(campaign.description, 'Some Sum')
        self.assertEqual(campaign.slug, 'argentina-fund')
        account.delete()    # cascades

    @patch('peacecorps.management.commands.sync_accounting.Campaign')
    def test_create_account_double(self, Campaign):
        """If an account with the same name already exists, create a distinct
        name based on project code"""
        row = {'PROJ_NAME': 'Peru Fund', 'PROJ_CODE': '777-CFD',
               'SUMMARY': 'Some Sum'}
        sync.create_account(row, None)
        row['PROJ_CODE'] = '778-CFD'
        sync.create_account(row, None)
        account = Account.objects.get(code='777-CFD')
        self.assertEqual(account.name, 'Peru Fund')
        account.delete()
        account = Account.objects.get(code='778-CFD')
        self.assertEqual(account.name, 'Peru Fund (778-CFD)')
        account.delete()

    def test_create_account_sector(self):
        """The creation of sectors creates a sector map, too"""
        row = {'PROJ_NAME': 'Renewal Fund', 'PROJ_CODE': 'SPF-REN',
               'COUNTRY_NAME': 'D/OSP/GGM', 'SUMMARY': 'Some Sum',
               'SECTOR': 'RENEW'}
        sync.create_account(row, None)
        account = Account.objects.get(code='SPF-REN')
        campaign = Campaign.objects.get(account=account)
        mapping = SectorMapping.objects.get(pk='RENEW')
        self.assertEqual(mapping.campaign, campaign)
        account.delete()    # cascades

    @patch('peacecorps.management.commands.sync_accounting.update_account')
    @patch('peacecorps.management.commands.sync_accounting.'
           + 'create_account')
    def test_command(self, create, update):
        """Verify CSV reading and that the update/create are called"""
        filedata = "PROJ_CODE,OTHER_FIELD,LAST_UPDATED_FROM_PAYGOV,REVENUE\n"
        filedata += '123-456,Some Content,2009-12-14 15:16:17,"1,234"\n'
        filedata += "nonexist,Not Here,2009-12-14 15:16:17,1.23\n"
        filedata += "111-222,Other Co¿ntent,2009-12-14 15:16:17,1.23\n"
        # Note the non-utf character ^
        csv_file_handle, csv_path = tempfile.mkstemp()
        with open(csv_file_handle, 'wb') as csv_file:
            csv_file.write(filedata.encode('iso-8859-1'))

        account456 = Account.objects.create(name='account1', code='123-456')
        account222 = Account.objects.create(name='account2', code='111-222')

        command = sync.Command()
        command.handle(csv_path)

        self.assertEqual(create.call_count, 1)
        self.assertEqual(update.call_count, 2)
        account222.delete()
        account456.delete()

    def test_account_type_country(self):
        row = {'PROJ_CODE': '123-CFD'}
        self.assertEqual(Account.COUNTRY, sync.account_type(row))
        row = {'PROJ_CODE': '111-222', 'SECTOR': 'None', 'PROJ_REQUEST': '0',
               'COUNTRY_NAME': 'RUSSIA', 'PCV_NAME': 'RUSSIA COUNTRY FUND'}
        self.assertEqual(Account.COUNTRY, sync.account_type(row))

    def test_account_type_memorial(self):
        row = {'PROJ_CODE': 'SPF-BOB', 'SECTOR': 'None', 'PROJ_REQUEST': '0',
               'COUNTRY_NAME': 'MOZAMBIQUE',
               'PROJ_NAME': 'Bob Jones Memorial Fund',
               'PCV_NAME': 'BOB JONES MEMORIAL FUND'}
        self.assertEqual(Account.MEMORIAL, sync.account_type(row))

    def test_account_type_sector(self):
        row = {'PROJ_CODE': 'SPF-YTH', 'SECTOR': 'Youth Development',
               'PROJ_REQUEST': '2550', 'COUNTRY_NAME': 'D/OSP/GGM',
               'PROJ_NAME': 'Youth Fund', 'PCV_NAME': 'The Youth Fund'}
        self.assertEqual(Account.SECTOR, sync.account_type(row))
        row = {'PROJ_CODE': 'SPF-YTH', 'SECTOR': 'Youth Development',
               'PROJ_REQUEST': '2550', 'COUNTRY_NAME': '',
               'PROJ_NAME': 'Youth Fund', 'PCV_NAME': 'YOUTH FUND'}
        self.assertEqual(Account.SECTOR, sync.account_type(row))

    def test_account_type_project(self):
        row = {'PROJ_CODE': '123-456', 'SECTOR': 'IT', 'PROJ_REQUEST': '0',
               'COUNTRY_NAME': 'FRANCE', 'PROJ_NAME': 'Proj Proj',
               'PCV_NAME': 'B. Smith', 'COMM_CONTRIB': ''}
        self.assertEqual(Account.PROJECT, sync.account_type(row))
        row = {'PROJ_CODE': '123-456-A', 'SECTOR': 'IT', 'PROJ_REQUEST': '0',
               'COUNTRY_NAME': 'FRANCE', 'PROJ_NAME': 'Proj Proj',
               'PCV_NAME': 'B. Smith', 'COMM_CONTRIB': '123.45'}
        self.assertEqual(Account.PROJECT, sync.account_type(row))
        row = {'PROJ_CODE': '123-456-A', 'SECTOR': 'IT', 'PROJ_REQUEST': '150',
               'COUNTRY_NAME': 'FRANCE', 'PROJ_NAME': 'Proj Proj',
               'PCV_NAME': 'B. Smith', 'COMM_CONTRIB': ''}
        self.assertEqual(Account.PROJECT, sync.account_type(row))

    def test_account_type_general(self):
        row = {'PROJ_CODE': 'PCF-GEN', 'SECTOR': 'None', 'PROJ_REQUEST': '0',
               'COUNTRY_NAME': 'D/OSP/GGM', 'PROJ_NAME': 'General Fund',
               'PCV_NAME': 'General Fund', 'COMM_CONTRIB': ''}
        self.assertEqual(Account.OTHER, sync.account_type(row))
