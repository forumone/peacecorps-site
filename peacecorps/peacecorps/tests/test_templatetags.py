from django.test import TestCase

from peacecorps.templatetags.humanize_cents import humanize_cents


class HumanizeTest(TestCase):
    def test_humanize_cents(self):
        """ The humanize_cents function converts an amount in cents into
        something that's human readable. """
        self.assertEqual('$0.00', humanize_cents(0))
        self.assertEqual('$0.12', humanize_cents(12))
        self.assertEqual('$1.23', humanize_cents(123))
        self.assertEqual('$12,345,678.90', humanize_cents(1234567890))
