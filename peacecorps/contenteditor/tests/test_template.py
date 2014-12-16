import json

from django.test import TestCase

from peacecorps.models import Vignette


class HeadingTests(TestCase):
    def test_override(self):
        """Verify that the custom header template is being used"""
        v = Vignette(slug='donate_landing_bottom', content=json.dumps({
            "data": [{"type": "heading",
                      "data": {"text": "All Projects &amp; Funds"}}]}))
        self.assertTrue('All Projects &amp; Funds' in v.content.html)
        self.assertTrue('<h1>' in v.content.html)
