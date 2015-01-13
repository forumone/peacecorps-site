import json
from urllib.parse import quote as urlquote

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from peacecorps.models import Account, Campaign, Country, FAQ, Project


class DonationsTests(TestCase):
    fixtures = ['countries.yaml']

    def setUp(self):
        self.proj_acc = Account.objects.create(
            name='PROJPROJ', code='PROJPROJ', category=Account.PROJECT,
            goal=200000)
        self.cmpn_acc = Account.objects.create(
            name='CMPNCMPN', code='CMPNCMPN', category=Account.OTHER)
        self.project = Project.objects.create(
            slug='sluggy', country=Country.objects.get(name='Egypt'),
            account=self.proj_acc, published=True)
        self.campaign = Campaign.objects.create(
            slug='cmpn', account=self.cmpn_acc)

    def tearDown(self):
        # Cascade
        self.cmpn_acc.delete()
        self.proj_acc.delete()

    def test_contribution_parameters(self):
        """ To get to the page where name, address are filled out before being
        shunted to pay.gov we need to pass the donation amount as a GET
        parameter and the project as a url param. Test that they show up on
        the payment page."""
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=20')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('$20.00' in content)
        self.assertTrue(self.proj_acc.code)     # Check that this is nonempty
        self.assertTrue(self.proj_acc.code in content)

        response = self.client.get(
            reverse('campaign form', kwargs={'slug': self.campaign.slug})
            + '?payment_amount=20.01')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('$20.01' in content)
        self.assertTrue(self.cmpn_acc.code)     # Check that this is nonempty
        self.assertTrue(self.cmpn_acc.code in content)

    def test_payment_type(self):
        """Check that the payment type values are rendered correctly."""
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=2000')
        content = response.content.decode('utf-8')
        self.assertTrue('id_payment_type_0' in content)
        self.assertTrue('id_payment_type_1' in content)
        self.assertTrue('CreditCard' in content)
        self.assertTrue('CreditACH' in content)

    def test_check_project_max(self):
        """Shouldn't be able to donate more than a project's remaining"""
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=2000')
        self.assertEqual(200, response.status_code)
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=2000.01')
        self.assertEqual(302, response.status_code)

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
            'payment_type': 'CreditCard',
            'information_consent': 'true',
            'random': 'randVal'}

        response = self.client.post(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=2000', form_data, HTTP_HOST='example.com')
        content = response.content.decode('utf-8')
        self.assertEqual(200, response.status_code)
        self.assertTrue('agency_tracking_id' in content)
        self.assertTrue('agency_id' in content)
        # this isn't a hidden value as it has the comma
        self.assertTrue('Anytown,' in content)
        self.assertTrue('name="random"' in content)
        self.assertTrue('value="randVal"' in content)

        #   Refetch the account so we can lookup its donorinfo
        account = Account.objects.get(pk=self.proj_acc.pk)
        self.assertEqual(1, len(account.donorinfos.all()))
        #   Also verify that the http host has been added
        donorinfo = account.donorinfos.get()
        self.assertTrue('://example.com' in donorinfo.xml)

    def test_review_page_not_appear(self):
        """The review page should *not* appear if a flag is provided"""
        form_data = {
            'payer_name': 'William Williams',
            'billing_address':  '1 Main Street',
            'billing_city': 'Anytown',
            'billing_state': 'MD',
            'billing_zip':  '20852',
            'country': 'USA',
            'payment_type': 'CreditCard',
            'information_consent': 'true'}

        response = self.client.post(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=2000', form_data)
        self.assertContains(response, 'agency_tracking_id')
        form_data['force_form'] = 'true'
        response = self.client.post(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=2000', form_data)
        self.assertNotContains(response, 'agency_tracking_id')

    def test_bad_request_donations(self):
        """ The donation information page should redirect if amount isn't
        included."""
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse('campaign form', kwargs={'slug': self.campaign.slug}))
        self.assertEqual(response.status_code, 302)

    def test_bad_amount(self):
        """If a non-numeric amount is entered, the donation form should
        redirect. Same applies with min/max bounds. Each of these should have
        a unique nonce to break the cache"""
        nonces = set()
        nonce_from = lambda r: r['LOCATION'].split('nonce=')[1].split('&')[0]
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=aaa')
        self.assertEqual(response.status_code, 302)
        nonces.add(nonce_from(response))
        response = self.client.get(
            reverse('campaign form', kwargs={'slug': self.campaign.slug})
            + '?payment_amount=aaa')
        self.assertEqual(response.status_code, 302)
        nonces.add(nonce_from(response))

        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=0.99')
        self.assertEqual(response.status_code, 302)
        nonces.add(nonce_from(response))
        response = self.client.get(
            reverse('project form', kwargs={'slug': self.project.slug})
            + '?payment_amount=10000')
        self.assertEqual(response.status_code, 302)
        nonces.add(nonce_from(response))

        self.assertEqual(len(nonces), 4)  # distinct nonces

    def test_completed_success(self):
        response = self.client.get(reverse('donation success'))
        self.assertEqual(response.status_code, 200)


class DonatePagesTests(TestCase):

    fixtures = ['tests.yaml']

    # Do the pages load without error?
    def test_pages_rendering(self):
        response = self.client.get('/donate/')
        self.assertEqual(response.status_code, 200)

    def test_project_rendering(self):
        response = self.client.get('/donate/project/brick-oven-bakery/')
        self.assertEqual(response.status_code, 200)

    def test_fund_rendering(self):
        response = self.client.get(reverse(
            'donate campaign', kwargs={'slug': 'health-hivaids-fund'}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('donate campaign',
                                           kwargs={'slug': 'cameroon'}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('donate campaign',
                    kwargs={'slug': 'stephanie-brown'}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('donate campaign',
                                           kwargs={'slug': 'peace-corps'}))
        self.assertEqual(response.status_code, 200)

    def test_project_fully_funded(self):
        """Verify that there's a submission button if the project is not
        funded and that this disappears if the project is funded"""
        project = Project.objects.get(slug='brick-oven-bakery')
        response = self.client.get(reverse('donate project',
                                           kwargs={'slug': project.slug}))
        self.assertContains(response, 'button')

        account = project.account
        old_amount, old_goal = account.current, account.goal
        account.current, account.goal = 1, 1
        account.save()
        response = self.client.get(reverse('donate project',
                                           kwargs={'slug': project.slug}))
        self.assertNotContains(response, 'button')
        account.current, account.goal = old_amount, old_goal
        account.save()

    def test_project_fund_prepopulation(self):
        """Prepopulate the form with amount from GET var"""
        response = self.client.get(
            reverse('donate project', kwargs={'slug': 'brick-oven-bakery'}),
            {'payment_amount': '12.34'})
        self.assertContains(response, '12.34')
        response = self.client.get(
            reverse('donate project', kwargs={'slug': 'brick-oven-bakery'}),
            {'payment_amount': '.95'})
        self.assertContains(response, '.95')
        self.assertContains(response, 'error')

        response = self.client.get(
            reverse('donate campaign', kwargs={'slug': 'peace-corps'}),
            {'payment_amount': '12.34'})
        self.assertContains(response, '12.34')
        response = self.client.get(
            reverse('donate campaign', kwargs={'slug': 'peace-corps'}),
            {'payment_amount': '10000'})
        self.assertContains(response, '10000')
        self.assertContains(response, 'error')

    def test_project_success_failure(self):
        response = self.client.get(
            reverse('project success', kwargs={'slug': 'nonproj'}))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('project failure', kwargs={'slug': 'nonproj'}),
            follow=True)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('project success',
                    kwargs={'slug': 'togo-clean-water-project'}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('project failure',
                    kwargs={'slug': 'togo-clean-water-project'}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_campaign_success_failure(self):
        response = self.client.get(
            reverse('campaign success', kwargs={'slug': 'nonproj'}))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('campaign failure', kwargs={'slug': 'nonproj'}),
            follow=True)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse('campaign success', kwargs={'slug': 'education-fund'}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('campaign failure', kwargs={'slug': 'education-fund'}),
            follow=True)
        self.assertEqual(response.status_code, 200)

    def test_post_redirect(self):
        """All POSTs to the project/campaign success pages should get
        redirected to the same page as a GET"""
        for proj_camp, slug in (('project', 'togo-clean-water-project'),
                                ('campaign', 'education-fund')):
            url = reverse(proj_camp + ' success', kwargs={'slug': slug})
            for enforce_csrf_checks in (False, True):
                client = Client(enforce_csrf_checks=enforce_csrf_checks)
                response = client.post(
                    url, data={'agency_tracking_id': 'NEVERUSED'})
                self.assertEqual(response.status_code, 302)
                self.assertTrue(url in response['LOCATION'])
                response = client.post(
                    url + '?something=else',
                    data={'agency_tracking_id': 'NEVERUSED'})
                self.assertEqual(response.status_code, 302)
                self.assertTrue(url in response['LOCATION'])
                self.assertTrue('?something=else' in response['LOCATION'])

    def test_failure_redirect(self):
        """All POSTS to the project/campaign failure page should get
        redirected to a page with a big 'sorry' banner"""
        for proj_camp, slug in (('project', 'togo-clean-water-project'),
                                ('campaign', 'education-fund')):
            url = reverse(proj_camp + ' failure', kwargs={'slug': slug})
            for enforce_csrf_checks in (False, True):
                client = Client(enforce_csrf_checks=enforce_csrf_checks)
                response = client.post(
                    url, data={'agency_tracking_id': 'NEVERUSED'}, follow=True)
                self.assertContains(response, 'Unfortunately')
                response = client.post(
                    url + '?something=else',
                    data={'agency_tracking_id': 'NEVERUSED'}, follow=True)
                self.assertContains(response, 'Unfortunately')

    def test_memorial_fund_name(self):
        response = self.client.get(reverse('donate special funds'))
        self.assertNotContains(response, 'Stephanie Brown Memorial Fund</h3>')
        self.assertContains(response, 'Stephanie Brown')

    def test_success_render(self):
        """Verify that the donor's name and share links are present"""
        url = reverse('campaign success', kwargs={'slug': 'education-fund'})
        url += '?donor_name=Billy'
        response = self.client.get(url, HTTP_HOST='example.com')
        self.assertContains(response, 'Thank you, Billy')
        self.assertContains(response, urlquote('http://example.com/'))


class FAQTests(TestCase):
    def answer(self, value):
        return json.dumps({"data": [{
            "type": "text", "data": {"text": value}}]})

    def test_presence(self):
        FAQ.objects.create(question="Q1Q1Q1", answer=self.answer("A1A1A1"))
        FAQ.objects.create(question="Q2Q2Q2", answer=self.answer("A2A2A2"))
        FAQ.objects.create(question="Q3Q3Q3", answer=self.answer("A3A3A3"))
        response = self.client.get(reverse('donate faqs'))
        self.assertContains(response, 'Q1Q1Q1')
        self.assertContains(response, 'Q2Q2Q2')
        self.assertContains(response, 'Q3Q3Q3')
        self.assertContains(response, 'A1A1A1')
        self.assertContains(response, 'A2A2A2')
        self.assertContains(response, 'A3A3A3')
        FAQ.objects.all().delete()
