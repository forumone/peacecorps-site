from django import template
from django.db import models
from django.utils.translation import ugettext as _

from django_jinja import library
import jinja2

register = template.Library()

@library.global_function
def get_config(model_name):
    model_class = models.get_model('site_configuration', model_name)
    if not model_class:
        raise template.TemplateSyntaxError(_(
            "Could not get the model name '%(model)s' from the application "
            "named '%(app)s'" % {
                'model': model_name,
                'app': app_label,
            }
        ))
    return model_class.get_obj()