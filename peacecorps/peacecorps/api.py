from django.conf import settings
from restless.views import Endpoint

from peacecorps.models import Account

class GetAccountPercent(Endpoint):
    def get(self, request):
        code = request.params.get('code')
        percent = Account.objects.get(code=code).percent_funded()
        return {'percent': '%s' % percent}