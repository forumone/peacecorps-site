from django.template import Template, Context
from django.test import TestCase

from django.test.utils import override_settings
from .models import SiteConfiguration


class SigletonTest(TestCase):

    def setUp(self):
        self.template = Template(
            '{% load singleton_tags %}'
            '{% get_site_configuration "tests.SiteConfiguration" as site_config  %}'
            '{{ site_config.site_name }}'
        )
        SiteConfiguration.objects.all().delete()

    def test_template_tag_renders_default_site_config(self):
        SiteConfiguration.objects.all().delete()
        # At this point, there is no configuration object and we expect a
        # one to be created automatically with the default name value as
        # defined in models.
        output = self.template.render(Context())
        self.assertIn('Default Config', output)

    def test_template_tag_renders_site_config(self):
        SiteConfiguration.objects.create(site_name='Test Config')
        output = self.template.render(Context())
        self.assertIn('Test Config', output)