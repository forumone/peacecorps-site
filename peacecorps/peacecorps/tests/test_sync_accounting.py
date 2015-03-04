from datetime import datetime
import logging
import tempfile
from unittest.mock import Mock, patch

from django.test import TestCase
from pytz import timezone
import json

from peacecorps.management.commands import sync_accounting as sync
from peacecorps.models import (
    Account, Campaign, Country, Donation, Project, SectorMapping)


class SyncAccountingTests(TestCase):
    def setUp(self):
        self.campaign_account = Account.objects.create(
            name='Information Technology', code='SPF-ITC')
        Campaign.objects.create(
            name='Technology', account=self.campaign_account)
        self.china = Country.objects.create(code='CHINA', name='China')

    def tearDown(self):
        self.campaign_account.delete()  # cascades
        self.china.delete()

    def test_datetime_from(self):
        """Test daylight savings conversions"""
        dt = sync.datetime_from('2012-09-09T00:00:00')    # EDT
        self.assertEqual(2012, dt.year)
        self.assertEqual(9, dt.month)
        self.assertEqual(10, dt.day)
        self.assertEqual(3, dt.hour)
        self.assertEqual(59, dt.minute)
        self.assertEqual(59, dt.second)
        self.assertEqual(dt.tzname(), 'UTC')

        dt = sync.datetime_from('2012-12-09T00:00:00')     # EST
        self.assertEqual(2012, dt.year)
        self.assertEqual(12, dt.month)
        self.assertEqual(10, dt.day)
        self.assertEqual(4, dt.hour)
        self.assertEqual(59, dt.minute)
        self.assertEqual(59, dt.second)
        self.assertEqual(dt.tzname(), 'UTC')

    def test_cents_from(self):
        self.assertEqual(123456789, sync.cents_from('1,234,567.89'))
        self.assertEqual(12300, sync.cents_from('123'))
        self.assertRaises(ValueError, sync.cents_from, '12.34.56')

    def test_update_account(self):
        """Use fake data to verify that amount fields are updated and old
        transactions are deleted"""
        acc222 = Account.objects.create(
            name='Account222', code='111-222', category=Account.PROJECT)

        tz = timezone('US/Eastern')
        before_donation = Donation.objects.create(account=acc222, amount=5432)
        before_donation.time = tz.localize(datetime(2009, 12, 14, 23, 59, 59))
        before_donation.save()
        after_donation = Donation.objects.create(account=acc222, amount=5432)
        after_donation.time = tz.localize(datetime(2009, 12, 15))
        after_donation.save()

        # First test with an empty LAST_UPDATED value
        row = {'LAST_UPDATED_FROM_PAYGOV': '', 'PROJ_REQ': '444',
               'UNIDENT_BAL': '110.7', 'OVERS_PART': '50'}
        sync.update_account(row, acc222)
        # All donations should remain
        self.assertNotEqual(
            None, Donation.objects.filter(pk=before_donation.pk).first())
        self.assertNotEqual(
            None, Donation.objects.filter(pk=after_donation.pk).first())
        # amount donated to should be updated
        self.assertEqual(33330, Account.objects.get(pk=acc222.pk).current)

        row = {'LAST_UPDATED_FROM_PAYGOV': '2009-12-14T00:00:00',
               'PROJ_REQ': '5,555.55', 'UNIDENT_BAL': '4,321.32',
               'OVERS_PART': '50'}
        sync.update_account(row, acc222)
        # before_donation should be deleted, but after_donation not
        self.assertEqual(
            None, Donation.objects.filter(pk=before_donation.pk).first())
        self.assertNotEqual(
            None, Donation.objects.filter(pk=after_donation.pk).first())

        # amount donated to should also be updated
        self.assertEqual(123423, Account.objects.get(pk=acc222.pk).current)

        # finally, verify that zero works
        row = {'LAST_UPDATED_FROM_PAYGOV': '2009-12-14T00:00:00',
               'PROJ_REQ': '5555.55', 'UNIDENT_BAL': '0', 'OVERS_PART': '50'}
        sync.update_account(row, acc222)
        self.assertEqual(555555, Account.objects.get(pk=acc222.pk).current)
        acc222.delete()

    def test_update_account_goal_community(self):
        """The account current, goal, and community should be set, as they can
        change with each pull from the financial system."""
        acc222 = Account.objects.create(
            name='Account222', code='111-222', category=Account.PROJECT,
            current=4500, goal=10000, community_contribution=5000)

        row = {'LAST_UPDATED_FROM_PAYGOV': '', 'PROJ_REQ': '90.00',
               'UNIDENT_BAL': '10', 'OVERS_PART': '25.75'}
        sync.update_account(row, acc222)
        latest = Account.objects.get(pk=acc222.pk)
        self.assertEqual(9000, latest.goal)
        self.assertEqual(8000, latest.current)
        self.assertEqual(2575, latest.community_contribution)
        acc222.delete()

    def test_create_pcpp(self):
        """Use fake data to generate a new pcpp"""
        account = Account(name='New Project Effort', code='098-765',
                          category=Account.PROJECT)
        row = {
            'PROJ_NO': '098-765', 'LOCATION': 'CHINA',
            'PROJ_NAME1': 'New Project Effort', 'PCV_NAME': 'IN Jones, B.',
            'STATE': 'IN', 'OVERS_PART': '1234.56', 'PROJ_REQ': '3,434',
            'UNIDENT_BAL': '1,111', 'SECTOR': 'IT', 'SUMMARY': 'sum sum sum'}
        issue_cache = Mock()
        issue_cache.find.return_value = Campaign.objects.get(name='Technology')
        sync.create_pcpp(account, row, issue_cache)
        project = Project.objects.get(title='New Project Effort')
        description = json.loads(project.description)
        description = description['data'][0]['data']['text']
        self.assertEqual(project.account.code, '098-765')
        self.assertEqual(project.country.name, 'China')
        self.assertEqual(project.volunteername, 'Jones, B.')
        self.assertEqual(project.volunteerhomestate, 'IN')
        self.assertEqual(project.account.community_contribution, 123456)
        self.assertEqual(project.account.goal, 343400)
        self.assertEqual(project.account.current, (343400 - 111100))
        self.assertEqual(project.overflow.name, 'Information Technology')
        self.assertEqual(project.campaigns.all()[0].name, 'Technology')
        self.assertEqual(description, 'sum sum sum')
        self.assertEqual(project.slug, 'new-project-effort')
        self.assertFalse(project.published)
        project.delete()
        account.delete()

    def test_create_pcpp_empty(self):
        """Community contribution might be empty"""
        account = Account(name='New Project Effort', code='098-765',
                          category=Account.PROJECT)
        row = {
            'PROJ_NO': '098-765', 'LOCATION': 'CHINA',
            'PROJ_NAME1': 'New Project Effort', 'PCV_NAME': 'IN Jones, B.',
            'STATE': 'IN', 'OVERS_PART': '', 'PROJ_REQ': '3,434',
            'UNIDENT_BAL': '1,111', 'SECTOR': 'IT', 'SUMMARY': 'sum sum sum'}
        issue_cache = Mock()
        issue_cache.find.return_value = Campaign.objects.get(name='Technology')
        sync.create_pcpp(account, row, issue_cache)
        project = Project.objects.get(title='New Project Effort')
        self.assertEqual(project.account.community_contribution, 0)
        self.assertEqual(project.account.goal, 343400)
        self.assertEqual(project.account.current, (343400 - 111100))
        account.delete()    # cascades

    def test_create_pcpp_failure(self):
        """Country and sector must be valid, lest nothing gets saved. An error
        should be logged in this situation"""
        count = Project.objects.count()
        issue_cache = Mock()
        issue_cache.find.return_value = Campaign.objects.get(name='Technology')
        row = {'LOCATION': 'NONEXISTENT', 'SECTOR': 'MOCKED', 'PROJ_NO': '111'}
        with self.assertLogs('peacecorps.sync_accounting',
                             level=logging.WARN) as logger:
            sync.create_pcpp(None, row, issue_cache)
        self.assertEqual(count, Project.objects.count())    # nothing created
        self.assertEqual(1, len(logger.output))
        self.assertTrue('NONEXISTENT' in logger.output[0])
        self.assertFalse('MOCKED' in logger.output[0])

        issue_cache.find.return_value = None
        row = {'LOCATION': 'IRELAND', 'SECTOR': 'MOCKED', 'PROJ_NO': '111'}
        with self.assertLogs('peacecorps.sync_accounting',
                             level=logging.WARN) as logger:
            sync.create_pcpp(None, row, issue_cache)
        self.assertEqual(count, Project.objects.count())    # nothing created
        self.assertEqual(2, len(logger.output))
        self.assertTrue('IRELAND' in logger.output[0])
        self.assertTrue('MOCKED' in logger.output[1])

    def test_create_pcpp_no_sector(self):
        """The ominous "None" sector has special significance"""
        account = Account(name='New Project Effort', code='098-765',
                          category=Account.PROJECT)
        row = {
            'PROJ_NO': '098-765', 'LOCATION': 'CHINA',
            'PROJ_NAME1': 'New Project Effort', 'PCV_NAME': 'IN Jones, B.',
            'STATE': 'IN', 'OVERS_PART': '', 'PROJ_REQ': '3,434',
            'UNIDENT_BAL': '1,111', 'SECTOR': 'None', 'SUMMARY': 'sum sum sum'}
        issue_cache = Mock()
        issue_cache.find.return_value = None
        sync.create_pcpp(account, row, issue_cache)
        project = Project.objects.get(title='New Project Effort')
        self.assertEqual(project.overflow, None)
        self.assertEqual(project.campaigns.all().count(), 0)
        account.delete()    # cascades

    @patch('peacecorps.management.commands.sync_accounting.create_pcpp')
    def test_create_account_project(self, create):
        """Test that execution is deferred to the create_pcpp method"""
        row = {'PROJ_NAME1': 'Some Proj', 'PROJ_NO': '121-212',
               'SECTOR': 'IT'}
        sync.create_account(row, None)
        self.assertTrue(create.called)
        account, row, issue_map = create.call_args[0]
        self.assertEqual(account.name, 'Some Proj')
        self.assertEqual(account.code, '121-212')
        self.assertEqual(account.category, Account.PROJECT)
        self.assertEqual(0, len(Account.objects.filter(pk=account.pk)))

    @patch('peacecorps.management.commands.sync_accounting.create_campaign')
    def test_create_account_campaign(self, create):
        """Test that execution is deferred to the create_campaign method"""
        """Campaigns should be created"""
        row = {'PROJ_NAME1': 'Argentina Fund', 'PROJ_NO': '789-CFD',
               'SUMMARY': 'Some Sum'}
        sync.create_account(row, None)
        self.assertTrue(create.called)
        account, row, name, acc_type = create.call_args[0]
        self.assertEqual(account.name, 'Argentina Fund')
        self.assertEqual(account.code, '789-CFD')
        self.assertEqual(account.category, Account.COUNTRY)
        self.assertEqual(0, len(Account.objects.filter(pk=account.pk)))

    @patch('peacecorps.management.commands.sync_accounting.Campaign')
    def test_create_account_double(self, Campaign):
        """If an account with the same name already exists, create a distinct
        name based on project code"""
        row = {'PROJ_NAME1': 'China Fund', 'PROJ_NO': '777-CFD',
               'SUMMARY': 'Some Sum', 'LOCATION': 'CHINA'}
        sync.create_account(row, None)
        row['PROJ_NO'] = '778-CFD'
        sync.create_account(row, None)
        account = Account.objects.get(code='777-CFD')
        self.assertEqual(account.name, 'China Fund')
        account.delete()
        account = Account.objects.get(code='778-CFD')
        self.assertEqual(account.name, 'China Fund (778-CFD)')
        account.delete()

    def test_create_account_sector(self):
        """The creation of sectors creates a sector map, too"""
        row = {'PROJ_NAME1': 'Renewal Fund', 'PROJ_NO': 'SPF-REN',
               'LOCATION': 'D/OSP/GGM', 'SUMMARY': 'Some Sum',
               'SECTOR': 'RENEW'}
        sync.create_account(row, None)
        account = Account.objects.get(code='SPF-REN')
        campaign = Campaign.objects.get(account=account)
        mapping = SectorMapping.objects.get(pk='RENEW')
        self.assertEqual(mapping.campaign, campaign)
        account.delete()    # cascades

    def test_create_campaign(self):
        """Verify that country funds have the correct country, and other funds
        have none. Also verify summary is json"""
        acc1 = Account.objects.create(name='acc1', code='111-111')
        row = {'PROJ_NAME1': 'China Fund', 'PROJ_NO': 'CFD-111',
               'LOCATION': 'CHINA', 'SUMMARY': 'Ssssss'}
        sync.create_campaign(acc1, row, 'China Fund', Account.COUNTRY)
        campaign = Campaign.objects.filter(name='China Fund').first()
        self.assertEqual(self.china.pk, campaign.country.pk)

        acc2 = Account.objects.create(name='acc2', code='222-222')
        row = {'PROJ_NAME1': 'Smith Memorial Fund', 'PROJ_NO': 'SPF-222',
               'SUMMARY': 'Ssssss'}
        sync.create_campaign(acc2, row, 'Smith Memorial Fund',
                             Account.MEMORIAL)
        campaign = Campaign.objects.filter(name='Smith Memorial Fund').first()
        self.assertEqual(None, campaign.country)
        self.assertEqual(
            {"data": [{"type": "text", "data": {"text": "Ssssss"}}]},
            json.loads(campaign.description))
        acc1.delete()
        acc2.delete()

    @patch('peacecorps.management.commands.sync_accounting.update_account')
    @patch('peacecorps.management.commands.sync_accounting.create_account')
    def test_handle(self, create, update):
        """Verify CSV reading and that the update/create are called. Also
        make sure that appropriate logs are created"""
        filedata = "PROJ_NO,SECTOR,OTHER_FIELD,PROJ_REQ,UNIDENT_BAL\n"
        filedata += '123-456,IT,Some Content,5555,"1,234"\n'
        filedata += "444-444,IT,Not Here,5.00,1.23\n"
        filedata += "111-222,IT,Other Co¿ntent,5,1.23\n"
        # Note the non-utf character ^
        csv_file_handle, csv_path = tempfile.mkstemp()
        with open(csv_file_handle, 'wb') as csv_file:
            csv_file.write(filedata.encode('iso-8859-1'))

        account456 = Account.objects.create(name='account1', code='123-456')
        account222 = Account.objects.create(name='account2', code='111-222')

        with self.assertLogs('peacecorps.sync_accounting') as logger:
            command = sync.Command()
            command.handle(csv_path)
        self.assertEqual(3, len(logger.output))
        self.assertTrue('123-456' in logger.output[0])
        self.assertTrue('Updating' in logger.output[0])
        self.assertTrue('5555' in logger.output[0])
        self.assertTrue('1,234' in logger.output[0])
        self.assertTrue('444-444' in logger.output[1])
        self.assertTrue('Creating' in logger.output[1])
        self.assertTrue('111-222' in logger.output[2])
        self.assertTrue('Updating' in logger.output[2])

        self.assertEqual(create.call_count, 1)
        self.assertEqual(update.call_count, 2)
        account222.delete()
        account456.delete()

    @patch('peacecorps.management.commands.sync_accounting.create_account')
    def test_process_rows_in(self, create):
        """Verify that projects are processed after sector funds"""
        rows = [
            {'PROJ_NO': '123-456', 'SECTOR': 'NEWSECTOR'},
            {'PROJ_NO': 'SPF-STR', 'SECTOR': 'NEWSECTOR', 'PROJ_NAME1': 'Proj',
             'LOCATION': 'D/OSP/GGM'}]
        sync.process_rows_in(rows)
        self.assertEqual(2, len(create.call_args_list))
        self.assertEqual(create.call_args_list[0][0][0]['PROJ_NO'], 'SPF-STR')
        self.assertEqual(create.call_args_list[1][0][0]['PROJ_NO'], '123-456')

    def test_account_type_country(self):
        row = {'PROJ_NO': '123-CFD'}
        self.assertEqual(Account.COUNTRY, sync.account_type(row))
        row = {'PROJ_NO': '111-222', 'SECTOR': 'None', 'PROJ_REQ': '0',
               'LOCATION': 'RUSSIA', 'PCV_NAME': 'RUSSIA COUNTRY FUND'}
        self.assertEqual(Account.COUNTRY, sync.account_type(row))

    def test_account_type_memorial(self):
        row = {'PROJ_NO': 'SPF-BOB', 'SECTOR': 'None', 'PROJ_REQ': '0',
               'LOCATION': 'MOZAMBIQUE',
               'PROJ_NAME1': 'Bob Jones Memorial Fund',
               'PCV_NAME': 'BOB JONES MEMORIAL FUND'}
        self.assertEqual(Account.MEMORIAL, sync.account_type(row))

    def test_account_type_sector(self):
        row = {'PROJ_NO': 'SPF-YTH', 'SECTOR': 'Youth Development',
               'PROJ_REQ': '2550', 'LOCATION': 'D/OSP/GGM',
               'PROJ_NAME1': 'Youth Fund', 'PCV_NAME': 'The Youth Fund'}
        self.assertEqual(Account.SECTOR, sync.account_type(row))
        row = {'PROJ_NO': 'SPF-YTH', 'SECTOR': 'Youth Development',
               'PROJ_REQ': '2550', 'LOCATION': '',
               'PROJ_NAME1': 'Youth Fund', 'PCV_NAME': 'YOUTH FUND'}
        self.assertEqual(Account.SECTOR, sync.account_type(row))

    def test_account_type_project(self):
        row = {'PROJ_NO': '123-456', 'SECTOR': 'IT', 'PROJ_REQ': '0',
               'LOCATION': 'FRANCE', 'PROJ_NAME1': 'Proj Proj',
               'PCV_NAME': 'B. Smith', 'OVERS_PART': ''}
        self.assertEqual(Account.PROJECT, sync.account_type(row))
        row = {'PROJ_NO': '123-456-A', 'SECTOR': 'IT', 'PROJ_REQ': '0',
               'LOCATION': 'FRANCE', 'PROJ_NAME1': 'Proj Proj',
               'PCV_NAME': 'B. Smith', 'OVERS_PART': '123.45'}
        self.assertEqual(Account.PROJECT, sync.account_type(row))
        row = {'PROJ_NO': '123-456-A', 'SECTOR': 'IT', 'PROJ_REQ': '150',
               'LOCATION': 'FRANCE', 'PROJ_NAME1': 'Proj Proj',
               'PCV_NAME': 'B. Smith', 'OVERS_PART': ''}
        self.assertEqual(Account.PROJECT, sync.account_type(row))

    def test_account_type_general(self):
        row = {'PROJ_NO': 'PCF-GEN', 'SECTOR': 'None', 'PROJ_REQ': '0',
               'LOCATION': 'D/OSP/GGM', 'PROJ_NAME1': 'General Fund',
               'PCV_NAME': 'General Fund', 'OVERS_PART': ''}
        self.assertEqual(Account.OTHER, sync.account_type(row))

    def test_clean_description(self):
        """Clean description replaces bad bytes and BRs"""
        text = '!@#$%^&*()_+1234567890-='
        self.assertEqual(sync.clean_description(text),
                         '!@#$%^&*()_+1234567890-=')

        text = "Darwin\u00c2\u00bfs Bulldog"
        self.assertEqual(sync.clean_description(text), "Darwin's Bulldog")

        text = "\n\r\nSome<BR><br /></BR>Text"
        self.assertEqual(sync.clean_description(text), "\n\r\nSome\n\nText")

    def test_trim_row(self):
        """Verify that rows are trimmed to the required length and logs are
        emitted"""
        row = {'PROJ_NO': 'A'*500, 'LOCATION': 'B'*500, 'CHANGE_DATE': 'C'*500,
               'PROJ_NAME1': 'D'*500, 'PCV_NAME': 'E'*500, 'SUMMARY': 'F'*500,
               'STATE': 'G'*500, 'OVERS_PART': 'H'*500, 'OVERS_PCT': 'I'*500,
               'PROJ_REQ': 'J'*500, 'UNIDENT_BAL': 'K'*500,
               'ATTRIBUTE4': 'L'*500, 'SECTOR': 'M'*500, 'SUB_SECTOR': 'N'*500,
               'LAST_UPDATED_FROM_PAYGOV': 'O'*500}
        should_trim = ('PROJ_NO', 'LOCATION', 'PROJ_NAME1', 'PCV_NAME',
                       'STATE', 'SECTOR')
        no_trim = [key for key in row if key not in should_trim]
        logger = Mock()
        row = sync.trim_row(row, logger)
        for key in should_trim:
            self.assertTrue(len(row[key]) < 500)
        for key in no_trim:
            self.assertEqual(len(row[key]), 500)
        self.assertEqual(logger.warning.call_count, len(should_trim))
