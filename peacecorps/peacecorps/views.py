from urllib.parse import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt

from peacecorps.forms import DonationAmountForm, DonationPaymentForm
from peacecorps.models import (
    Account, Campaign, FeaturedCampaign, FeaturedProjectFrontPage,
    Issue, humanize_amount, Project, Vignette)
from peacecorps.payxml import convert_to_paygov


def donation_payment(request):
    """ Collect donor contact information. """

    amount = request.GET.get('amount', None)
    project_code = request.GET.get('project', None)

    if amount is None or project_code is None:
        return HttpResponseBadRequest(
            'amount and project must be provided.')
    try:
        amount = int(amount)
    except ValueError:
        return HttpResponseBadRequest('amount must be an integer value')

    account = Account.objects.filter(code=project_code).first()
    if not account:
        return HttpResponseBadRequest('Invalid project')

    readable_amount = humanize_amount(amount)

    if request.method == 'POST':
        form = DonationPaymentForm(request.POST)

        if form.is_valid():
            data = {}
            for k, v in form.cleaned_data.items():
                data[k] = v
            return donation_payment_review(request, data, account)
    else:
        data = {'payment_amount': amount, 'project_code': project_code}
        form = DonationPaymentForm(initial=data)

    return render(
        request, 'donations/donation_payment.jinja',
        {
            'form': form,
            'amount': readable_amount,
            'project_code': project_code
        })


def donation_payment_review(request, data, account):
    """Save the payment information for future access; provide the user with a
    form that sends them over to pay.gov"""
    callback_base = request.scheme + "://" + request.get_host()
    paygov = convert_to_paygov(data, account, callback_base)
    paygov.save()

    return render(
        request,
        'donations/review_payment.jinja',
        {
            'data': data,
            'agency_id': settings.PAY_GOV_AGENCY_ID,
            'agency_tracking_id': paygov.agency_tracking_id,
            'app_name': settings.PAY_GOV_APP_NAME,
            'oci_servlet_url': settings.PAY_GOV_OCI_URL,
        })


def donate_landing(request):
    """First page for the donations section"""
    featuredprojects = list(map(
        lambda fp: fp.project,
        FeaturedProjectFrontPage.objects.select_related(
            'project__featured_image')))
    projects = Project.published_objects.select_related('country', 'account')

    try:
        featuredcampaign = FeaturedCampaign.objects.get(id=1).campaign
    except FeaturedCampaign.DoesNotExist:
        featuredcampaign = None

    return render(
        request,
        'donations/donate_landing.jinja',
        {
            'top_vignette': Vignette.for_slug('donate_landing_top'),
            'bottom_vignette': Vignette.for_slug('donate_landing_bottom'),
            'featuredcampaign': featuredcampaign,
            'sectors': Campaign.objects.filter(
                campaigntype=Campaign.SECTOR).order_by('name'),
            'featuredprojects': featuredprojects,
            'projects': projects,
            'humanize_amount': humanize_amount,
        })


def donate_project(request, slug):
    """A profile for each project. Also includes a donation form"""
    project = get_object_or_404(
        Project.published_objects.select_related(
            'volunteerpicture', 'featured_image', 'account', 'overflow'),
        slug=slug)
    if request.method == 'POST':
        form = DonationAmountForm(data=request.POST)
        if form.is_valid():
            if project.account.funded() and project.overflow:
                code = project.overflow.code
            else:
                code = project.account.code
            params = {'project': code,
                      # convert back into cents
                      'amount': int(round(
                          form.cleaned_data['payment_amount'] * 100))}
            return HttpResponseRedirect(
                reverse('donations_payment') + '?' + urlencode(params))
    else:
        form = DonationAmountForm()

    return render(
        request,
        'donations/donate_project.jinja',
        {
            'project': project,
            'account': project.account,
            'donate_form': form,
            'humanize_amount': humanize_amount,
        })


def donate_projects_funds(request):
    """
    The page that displays a sorter for all projects, issues, volunteers.
    """
    countries = Campaign.objects.filter(
        campaigntype=Campaign.COUNTRY).order_by('name')
    issues = Issue.objects.all().order_by('name')
    projects = Project.published_objects.select_related(
        'country', 'account').order_by('volunteername')

    return render(
        request,
        'donations/donate_all.jinja',
        {
            'countries': countries,
            'issues': issues,
            'projects': projects
        })


def special_funds(request):
    """Contains general, global, and memorial funds"""
    general_funds = Campaign.objects.filter(
        campaigntype=Campaign.GENERAL).order_by('pk')
    memorial_funds = Campaign.objects.filter(campaigntype=Campaign.MEMORIAL)
    # Quick hack to pull out the volunteer's name. Replace when we have a new
    # model
    for fund in memorial_funds:
        if fund.name.endswith('Memorial Fund'):
            fund.memorial_name = fund.name[:-len("Memorial Fund")].strip()
        else:
            fund.memorial_name = fund.name.strip()
        name_parts = fund.memorial_name.split(' ')
        fund.sort_name = " ".join(name_parts[-1:] + name_parts[:-1])
    memorial_funds = sorted(memorial_funds, key=lambda f: f.sort_name)
    return render(request, "donations/special_funds.jinja", {
        "general_funds": general_funds, "memorial_funds": memorial_funds})


def fund_detail(request, slug):
    campaign = get_object_or_404(Campaign.objects.select_related('account'),
                                 slug=slug)
    if request.method == "POST":
        form = DonationAmountForm(data=request.POST)
        if form.is_valid():
            params = {'project': campaign.account.code,
                      # convert back into cents
                      'amount': int(round(
                          form.cleaned_data['payment_amount'] * 100))}
            return HttpResponseRedirect(
                reverse('donations_payment') + '?' + urlencode(params))
    else:
        form = DonationAmountForm()

    return render(
        request,
        'donations/fund_detail.jinja',
        {
            'campaign': campaign,
            'account': campaign.account,
            'donate_form': form,
        })


class ProjectReturn(DetailView):
    queryset = Project.objects.select_related(
        'account', 'country', 'featured_image', 'overflow',
        'volunteerpicture')

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.path)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ProjectReturn, self).dispatch(*args, **kwargs)


class CampaignReturn(DetailView):
    queryset = Campaign.objects.select_related('account', 'featured_image')

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.path)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CampaignReturn, self).dispatch(*args, **kwargs)
