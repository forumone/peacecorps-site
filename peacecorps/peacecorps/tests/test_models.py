from django.test import TestCase

from peacecorps import models


class HumanizeTest(TestCase):
    def test_humanize_amount(self):
        self.assertEqual('$0.00', models.humanize_amount(0))
        self.assertEqual('$0.12', models.humanize_amount(12))
        self.assertEqual('$1.23', models.humanize_amount(123))
        self.assertEqual('$12,345,678.90', models.humanize_amount(1234567890))
