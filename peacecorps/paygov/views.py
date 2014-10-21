import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
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
        info = get_object_or_404(
            DonorInfo, pk=request.POST.get('agency_tracking_id'))
        return HttpResponse(info.xml, content_type='text/xml')
