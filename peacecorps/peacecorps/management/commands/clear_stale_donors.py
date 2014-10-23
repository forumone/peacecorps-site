from django.core.management.base import BaseCommand
from django.utils import timezone

from peacecorps.models import DonorInfo


class Command(BaseCommand):
    help = "Clear donor info structures that have expired"

    def handle(self, *args, **kwargs):
        DonorInfo.objects.filter(expires_at__lte=timezone.now()).delete()
