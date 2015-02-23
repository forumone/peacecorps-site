from django.db import models

from site_configuration.models import SingletonModel


class Name(SingletonModel):
    site_name = models.CharField(max_length=255, default='Default Config')