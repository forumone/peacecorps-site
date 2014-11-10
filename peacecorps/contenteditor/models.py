from django.conf import settings
from django.db import models


# Create your models here.
class ExtraUserFields(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    last_password_change = models.DateTimeField()
