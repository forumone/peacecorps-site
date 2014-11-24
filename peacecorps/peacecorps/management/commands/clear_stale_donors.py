import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from peacecorps.models import DonorInfo


class Command(BaseCommand):
    help = "Clear donor info structures that have expired"

    def handle(self, *args, **kwargs):
        queryset = DonorInfo.objects.filter(expires_at__lte=timezone.now())
        count = queryset.count()
        if count:
            queryset.delete()
            logging.getLogger('peacecorps.clear_stale_donors').info(
                "Deleted %s expired donor info objects", count)
