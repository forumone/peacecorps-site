from django.test import TestCase

from peacecorps import models


class HumanizeTest(TestCase):
    def test_humanize_amount(self):
        self.assertEqual('$0.00', models.humanize_amount(0))
        self.assertEqual('$0.12', models.humanize_amount(12))
        self.assertEqual('$1.23', models.humanize_amount(123))
        self.assertEqual('$12,345,678.90', models.humanize_amount(1234567890))


class AccountTest(TestCase):
    def test_funded(self):
        account = models.Account()
        self.assertFalse(account.funded())
        account.current = 100
        self.assertFalse(account.funded())
        account.goal = 101
        self.assertFalse(account.funded())
        account.goal = 100
        self.assertTrue(account.funded())
        account.goal = 99
        self.assertTrue(account.funded())

    def test_track_total(self):
        """Use fake data to verify that account totals are being
        kept up-to-date"""
        def makedonation(acct, amount):
            donation = models.Donation.objects.create(
                account=acct, amount=amount)
            donation.save()
            return donation

        acc1 = models.Account.objects.create(
            name='Account1', code='112-358', current=150)
        makedonation(acc1, 75)
        makedonation(acc1, 100)
        makedonation(acc1, 1)

        self.assertEqual(326, acc1.total())

    def test_percent_funded(self):
        account = models.Account()
        account.donations = []
        account.current = 30
        account.community_contribution = 10
        account.goal = 70
        self.assertEqual(50, account.percent_funded())
        account.current += 20
        self.assertEqual(75, account.percent_funded())

    def test_community_funded(self):
        account = models.Account()
        account.community_contribution = 80
        account.goal = 80
        self.assertEqual(50, account.percent_community_funded())
        account.community_contribution = 100
        self.assertEqual(55.56, account.percent_community_funded())

class ProjectTests(TestCase):
    fixtures = ['countries.yaml']

    def test_published(self):
        """Publish is not set by default"""
        account = models.Account.objects.create(name='Acc', code='ACC')
        models.Project.objects.all().delete()
        proj = models.Project.objects.create(
            country=models.Country.objects.get(name='Mexico'),
            account=account)
        self.assertFalse(proj.published)
        self.assertEqual(1, len(models.Project.objects.all()))
        self.assertEqual(0, len(models.Project.published_objects.all()))

        proj.published = True
        proj.save()
        self.assertEqual(1, len(models.Project.objects.all()))
        self.assertEqual(1, len(models.Project.published_objects.all()))

        proj.delete()
        account.delete()

    def test_slug_collision(self):
        """Project slug should be derived from title, yet unique"""
        account1 = models.Account.objects.create(name='Acc', code='ACC')
        account2 = models.Account.objects.create(name='Acc2', code='ACC2')
        country = models.Country.objects.get(name='Mexico')
        proj1 = models.Project.objects.create(
            title='Project', country=country, account=account1)
        proj2 = models.Project.objects.create(
            title='Project', country=country, account=account2)
        self.assertEqual(proj1.slug, 'project')
        self.assertEqual(proj2.slug, 'project' + str(proj1.id))
        account1.delete()
        account2.delete()
