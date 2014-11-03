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
