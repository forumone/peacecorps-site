import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from paygov.models import DonorInfo


@csrf_exempt
def data(request):
    logger = logging.getLogger('paygov.data')
    logger.debug(request)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.POST.get('agency_tracking_id'):
        return HttpResponseBadRequest('Missing agency_tracking_id')
    else:
        info = DonorInfo.objects.filter(
            pk=request.POST.get('agency_tracking_id')).first()
        if not info:
            return HttpResponseBadRequest('Bad agency_tracking_id')
        else:
            return HttpResponse(info.xml)
