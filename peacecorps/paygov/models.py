from datetime import timedelta

from django.db import models
from django.utils import timezone


def default_expire_time():
    return timezone.now() + timedelta(minutes=20)


class DonorInfo(models.Model):
    """Represents a blob of donor information which will be requested by
    pay.gov. We need to limit accessibility as it contains PII"""
    agency_tracking_id = models.CharField(max_length=21, primary_key=True)
    fund = models.ForeignKey('peacecorps.Fund', related_name='donorinfos')
    xml = models.TextField()    # @todo: encrypt
    expires_at = models.DateTimeField(default=default_expire_time)
