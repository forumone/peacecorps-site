from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from peacecorps.models import Fund, Project
from peacecorps.views import humanize_amount


class DonationsTests(TestCase):
    def setUp(self):
        self.fund = Fund.objects.create(fundcode='FUNDFUND')

    def tearDown(self):
        self.fund.delete()

    def test_contribution_parameters(self):
        """ To get to the page where name, address are filled out before being
        shunted to pay.gov we need to pass the donation amount and project code
        as GET parameters. This makes sure they show up on the payment page.
        """

        response = self.client.get(
            '/donations/contribute/?amount=2000&project=' + self.fund.fundcode)
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('$20.00' in content)
        self.assertTrue(self.fund.fundcode)     # Check that this is nonempty
        self.assertTrue(self.fund.fundcode in content)

    def test_payment_type(self):
        """Check that the payment type values are rendered correctly."""

        response = self.client.get(
            '/donations/contribute/?amount=2000&project=' + self.fund.fundcode)
        content = response.content.decode('utf-8')
        self.assertTrue('id_payment_type_0' in content)
        self.assertTrue('id_payment_type_1' in content)
        self.assertTrue('CreditCard' in content)
        self.assertTrue('CreditACH' in content)

    def test_review_page(self):
        """ Test that the donation review page renders with the required
        elements. """

        form_data = {
            'payer_name': 'William Williams',
            'billing_address':  '1 Main Street',
            'billing_city': 'Anytown',
            'billing_state': 'MD',
            'billing_zip':  '20852',
            'country': 'USA',
            'payment_amount': 2000,
            'project_code': 'PC-SEC01',
            'donor_type': 'Individual',
            'payment_type': 'CreditCard',
            'information_consent': 'vol-consent-yes'}

        response = self.client.post(
            '/donations/contribute/?amount=2000&project=' + self.fund.fundcode,
            form_data)
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('agency_tracking_id' in content)
        self.assertTrue('agency_id' in content)
        self.assertTrue('1 Main Street' in content)
        self.assertTrue('Anytown' in content)
        self.assertTrue('MD' in content)
        self.assertTrue('20852' in content)

        #   Refetch the fund so we can lookup its donorinfo
        fund = Fund.objects.get(pk=self.fund.pk)
        self.assertEqual(1, len(fund.donorinfos.all()))

    def test_humanize_amount(self):
        """ The humanize_amount function converts an amount in cents into
        something that's human readable. """
        self.assertEqual(humanize_amount(1520), '$15.20')
        self.assertEqual(humanize_amount(0), '$0.00')

    def test_bad_request_donations(self):
        """ The donation information page should 400 if donation amount and
        project code aren't included. """
        response = self.client.get('/donations/contribute')
        self.assertEqual(response.status_code, 400)

    def test_bad_amount(self):
        """ If a non-integer amount is entered, the donations/contribute page
        should 400. """

        response = self.client.get(
            '/donations/contribute/?amount=aaa&project_code=154')
        self.assertEqual(response.status_code, 400)

    def test_completed_success(self):
        response = self.client.get(reverse('donation success'))
        self.assertEqual(response.status_code, 200)

    def test_completed_failure(self):
        response = self.client.get(reverse('donation failure'))
        self.assertEqual(response.status_code, 200)


class DonatePagesTests(TestCase):

    fixtures = ['tests.yaml']

    def setUp(self):
        self.client = Client()

    # Do the pages load without error?
    def test_pages_rendering(self):
        response = self.client.get('/donate')
        self.assertEqual(response.status_code, 200)

    def test_issue_rendering(self):
        response = self.client.get('/donate/issue/health')
        self.assertEqual(response.status_code, 200)

    def test_project_rendering(self):
        response = self.client.get('/donate/project/brick-oven-bakery')
        self.assertEqual(response.status_code, 200)

    def test_country_rendering(self):
        response = self.client.get('/donate/country/cameroon')
        self.assertEqual(response.status_code, 200)

    def test_countries_rendering(self):
        response = self.client.get('/donate/countries')
        self.assertEqual(response.status_code, 200)

    def test_project_form_empty_amount(self):
        response = self.client.post('/donate/project/brick-oven-bakery',
                                    {'top-presets': 'custom',
                                     'top-payment_amount': ''})
        self.assertEqual(response.status_code, 200)

    def test_project_form_low_amount(self):
        response = self.client.post('/donate/project/brick-oven-bakery',
                                    {'top-presets': 'custom',
                                     'top-payment_amount': '0.99'})
        self.assertEqual(response.status_code, 200)

    def test_project_form_high_amount(self):
        response = self.client.post('/donate/project/brick-oven-bakery',
                                    {'top-presets': 'custom',
                                     'top-payment_amount': '10000.00'})
        self.assertEqual(response.status_code, 200)

    def test_project_form_redirect_all(self):
        """When selecting the fund-remaining-amount option, everything should
        work"""
        response = self.client.post('/donate/project/brick-oven-bakery',
                                    {'top-presets': 'preset-all'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue("220000" in response['Location'])
        fundcode = Project.objects.get(slug='brick-oven-bakery').fund.fundcode
        self.assertTrue(fundcode)
        self.assertTrue(fundcode in response['Location'])

    def test_project_form_redirect_custom(self):
        """When selecting the fund-a-custom-amount option, everything should
        work"""
        response = self.client.post('/donate/project/brick-oven-bakery',
                                    {'top-presets': 'custom',
                                     'top-payment_amount': '123.45'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue("12345" in response['Location'])
        fundcode = Project.objects.get(slug='brick-oven-bakery').fund.fundcode
        self.assertTrue(fundcode)
        self.assertTrue(fundcode in response['Location'])

    def test_project_form_redirect_bottom(self):
        """Despite the top form being invalid, if the bottom is, we should
        still redirect"""
        response = self.client.post('/donate/project/brick-oven-bakery',
                                    {'top-presets': 'custom',
                                     'bottom-presets': 'preset-all'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue("220000" in response['Location'])
        fundcode = Project.objects.get(slug='brick-oven-bakery').fund.fundcode
        self.assertTrue(fundcode)
        self.assertTrue(fundcode in response['Location'])
