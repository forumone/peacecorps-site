from django.db import models


class DonorInfo(models.Model):
    """Represents a blob of donor information which will be requested by
    pay.gov. We need to limit accessibility as it contains PII"""
    agency_tracking_id = models.CharField(max_length=21, primary_key=True)
    fund = models.ForeignKey('peacecorps.Fund')
    xml = models.TextField()    # @todo: encrypt
