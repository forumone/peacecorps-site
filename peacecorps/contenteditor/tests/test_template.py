from django.test import TestCase

from peacecorps.models import Vignette


class HeadingTests(TestCase):
    fixtures = ['vignettes']

    def test_override(self):
        """Verify that the custom header template is being used"""
        v = Vignette.for_slug('donate_landing_bottom')
        self.assertTrue('All Projects &amp; Funds' in v.content.html)
        self.assertTrue('<h1>' in v.content.html)
