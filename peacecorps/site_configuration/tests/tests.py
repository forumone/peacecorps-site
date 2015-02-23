from django.template import Template, Context
from django.test import TestCase

from django.test.utils import override_settings
from .models import Name


class SigletonTest(TestCase):

    def setUp(self):
        self.template = Template(
            "{{ get_config('Name').site_name }}"
        )

    def renders_site_config(self):
        Name.objects.create(site_name='Test Config')
        output = self.template.render(Context())
        self.assertIn('Test Config', output)