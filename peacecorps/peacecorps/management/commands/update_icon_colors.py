from django.core.management.base import BaseCommand

from peacecorps.models import Issue


class Command(BaseCommand):
    help = """
        Save color versions of each of the issue icons. Useful if these
        colors have changed"""

    def handle(self, *args, **kwargs):
        for issue in Issue.objects.all().iterator():
            issue.save()
