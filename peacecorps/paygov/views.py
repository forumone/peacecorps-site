import logging
import re

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from peacecorps.models import Donation, DonorInfo


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


@csrf_exempt
def results(request):
    logger = logging.getLogger('paygov.results')
    logger.debug(request)
    message = 'OK'
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    info = DonorInfo.objects.select_related('account').filter(
        pk=request.POST.get('agency_tracking_id')).first()
    if not info:
        message = 'Invalid agency_tracking_id'
    elif not request.POST.get('payment_status'):
        message = 'Missing payment_status'
    # Transaction was canceled or had another error
    elif request.POST.get('payment_status') != 'Completed':
        message = request.POST.get('error_message', 'Unknown error')
        logger.info("Transaction %s: %s", request.POST.get('payment_status'),
                    message)
        info.delete()
    elif not request.POST.get('payment_amount'):
        message = 'Missing payment_amount'
    elif not re.match(r'^\d+(\.\d*)?$', request.POST.get('payment_amount')):
        message = 'Invalid payment_amount'
    # Successful transaction
    else:
        donation = Donation(
            amount=int(float(request.POST.get('payment_amount'))*100))
        donation.account_id = info.account_id
        donation.save()
        info.delete()
        logger.info("Transaction success: %s cents to %s", donation.amount,
                    info.account.code)
    return HttpResponse('response_message=' + message,
                        content_type='text/plain')
