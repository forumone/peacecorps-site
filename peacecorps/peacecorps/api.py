from restless.views import Endpoint

from peacecorps.models import Account


class GetAccountPercent(Endpoint):
    def get(self, request, slug):
        percent = Account.objects.get(code=slug).percent_raised()
        return {'percent': percent}
