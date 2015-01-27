from unittest.mock import Mock

from django.test import TestCase

from peacecorps import api
from peacecorps.models import (
    Account, Campaign, Country, DonorInfo, Media, Project)


class ProjectDetailTests(TestCase):
    def test_serialize_volunteer(self):
        project = Project(volunteername='B. Smith',
                          volunteerhomestate='ID')
        result = api._serialize_volunteer(project)
        self.assertEqual(result['name'], 'B. Smith')
        self.assertEqual(result['homestate'], 'ID')
        self.assertEqual(result['picture'], None)

        project.volunteerpicture = Media()
        project.volunteerpicture.file = Mock()
        project.volunteerpicture.file.url = 'urlhere'
        result = api._serialize_volunteer(project)
        self.assertEqual(result['name'], 'B. Smith')
        self.assertEqual(result['homestate'], 'ID')
        self.assertEqual(result['picture'], 'urlhere')

    def test_serialize_account(self):
        account = Account()
        project = Project(account=account)

        result = api._serialize_account(project)
        self.assertEqual(result['goal'], None)
        self.assertEqual(result['community_contribution'], None)
        self.assertEqual(result['total_donated'], 0)
        self.assertEqual(result['total_raised'], 0)
        self.assertEqual(result['total_cost'], 0)
        self.assertEqual(result['percent_raised'], 0)
        self.assertEqual(result['percent_community'], 0)
        self.assertEqual(result['remaining'], 0)
        self.assertEqual(result['funded'], False)

        account.goal = 2400
        account.community_contribution = 600
        account.current = 900
        result = api._serialize_account(project)
        self.assertEqual(result['goal'], 2400)
        self.assertEqual(result['community_contribution'], 600)
        self.assertEqual(result['total_donated'], 900)
        self.assertEqual(result['total_raised'], 1500)
        self.assertEqual(result['total_cost'], 3000)
        self.assertEqual(result['percent_raised'], 50)
        self.assertEqual(result['percent_community'], 20)
        self.assertEqual(result['remaining'], 1500)
        self.assertEqual(result['funded'], False)

        account.current = 2400
        result = api._serialize_account(project)
        self.assertEqual(result['total_donated'], 2400)
        self.assertEqual(result['total_raised'], 3000)
        self.assertEqual(result['percent_raised'], 100)
        self.assertEqual(result['remaining'], 0)
        self.assertEqual(result['funded'], True)

    def test_serialize(self):
        country = Country(name='Awesomeland')
        account = Account()
        project = Project(account=account, country=country)
        pd = api.ProjectDetail()

        result = pd.serialize(project)
        self.assertEqual(result['title'], '')
        self.assertEqual(result['tagline'], None)
        self.assertEqual(result['country'], 'Awesomeland')
        self.assertEqual(result['featured_image'], None)

        project.title = 'SomeTitle'
        project.tagline = 'SomeTagline'
        project.featured_image = Media()
        project.featured_image.file = Mock()
        project.featured_image.file.url = 'urlhere'
        result = pd.serialize(project)
        self.assertEqual(result['title'], 'SomeTitle')
        self.assertEqual(result['tagline'], 'SomeTagline')
        self.assertEqual(result['featured_image'], 'urlhere')


class ProjectDonationTests(TestCase):
    fixtures = ['countries']

    def test_amount_errors(self):
        pd = api.ProjectDonation()
        host = 'example.com'
        account = Account(goal=200, current=0)
        # no payment amount
        data = {}
        result = pd.errors_or_paygov(account, data, host)
        self.assertEqual(result.status_code, 400)
        self.assertTrue('amount' in result.content.decode('utf-8'))

        # low payment amount
        data['payment_amount'] = '0.99'
        result = pd.errors_or_paygov(account, data, host)
        self.assertEqual(result.status_code, 400)
        self.assertTrue('amount' in result.content.decode('utf-8'))

        # high payment amount
        data['payment_amount'] = '10000'
        result = pd.errors_or_paygov(account, data, host)
        self.assertEqual(result.status_code, 400)
        self.assertTrue('amount' in result.content.decode('utf-8'))

        # too much for project
        data['payment_amount'] = '3'
        result = pd.errors_or_paygov(account, data, host)
        self.assertEqual(result.status_code, 400)
        self.assertTrue('amount' in result.content.decode('utf-8'))

        # passes the amount test but not the donor form
        data['payment_amount'] = '2'
        result = pd.errors_or_paygov(account, data, host)
        self.assertEqual(result.status_code, 400)
        self.assertTrue('amount' not in result.content.decode('utf-8'))

        # account is full
        account.current = 200
        result = pd.errors_or_paygov(account, data, host)
        self.assertEqual(result.status_code, 400)
        self.assertTrue('amount' in result.content.decode('utf-8'))

    def test_errors_or_paygov_success(self):
        pd = api.ProjectDonation()
        host = 'example.com'
        account = Account.objects.create(goal=200, current=0)
        Campaign.objects.create(slug='cmpn', account=account)
        data = {
            'payment_amount': '2',
            'payer_name': 'William Williams',
            'billing_address':  '1 Main Street',
            'billing_city': 'Anytown',
            'billing_state': 'MD',
            'billing_zip':  '20852',
            'country': 'USA',
            'payment_type': 'CreditCard',
            'information_consent': 'true'}
        self.assertEqual(0, len(DonorInfo.objects.all()))
        with self.settings(PAY_GOV_AGENCY_ID='pgai',
                           PAY_GOV_APP_NAME='pgan',
                           PAY_GOV_OCI_URL='pgou'):
            result = pd.errors_or_paygov(account, data, host)
            self.assertEqual('pgai', result['agency_id'])
            self.assertEqual('pgan', result['app_name'])
            self.assertEqual('pgou', result['oci_servlet_url'])

            paygov = DonorInfo.objects.all()[0]
            self.assertEqual(paygov.agency_tracking_id,
                             result['agency_tracking_id'])
            paygov.delete()
        account.delete()
