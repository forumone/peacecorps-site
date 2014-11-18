from django.conf import settings
from restless.views import Endpoint

from peacecorps.models import Account

class GetAccountPercent(Endpoint):
    def get(self, request, slug):
        percent = Account.objects.get(code=slug).percent_funded()
        return {'percent': percent}