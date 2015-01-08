from urllib.parse import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_exempt

from peacecorps.forms import DonationAmountForm, DonationPaymentForm
from peacecorps.models import (
    Account, Campaign, FAQ, FeaturedCampaign, FeaturedProjectFrontPage,
    Issue, Project, Vignette)
from peacecorps.payxml import convert_to_paygov


def donation_payment(request):
    """ Collect donor contact information. """

    amount = request.GET.get('amount')
    if amount is None:
        return HttpResponseBadRequest('amount must be provided.')
    elif not amount.isdigit():
        return HttpResponseBadRequest('amount must be an integer value')
    else:
        amount = int(amount)

    project_code = request.GET.get('project')
    if project_code is None:
        return HttpResponseBadRequest('project must be provided.')
    account = Account.objects.filter(code=project_code).first()
    if not account:
        return HttpResponseBadRequest('Invalid project')
    project = account.project_set.first()

    context = {
        'amount': amount,
        'project_code': project_code,
        'project': project,
        'account_name': account.name,
        'agency_id': settings.PAY_GOV_AGENCY_ID,
        'app_name': settings.PAY_GOV_APP_NAME,
        'oci_servlet_url': settings.PAY_GOV_OCI_URL,
    }

    if request.method == 'POST':
        form = DonationPaymentForm(request.POST)
    else:
        data = {'payment_amount': amount, 'project_code': project_code}
        form = DonationPaymentForm(initial=data)
    context['form'] = form

    if form.is_valid() and request.POST.get('force_form') != 'true':
        data = {k: v for k, v in form.cleaned_data.items()}
        paygov = convert_to_paygov(
            data, account, "https://" + request.get_host())
        paygov.save()
        context['data'] = data
        context['agency_tracking_id'] = paygov.agency_tracking_id
        return render(request, 'donations/checkout_review.jinja', context)
    else:
        return render(request, 'donations/checkout_form.jinja', context)


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
            'title': 'Donate',
            'top_vignette': Vignette.for_slug('donate_landing_top'),
            'bottom_vignette': Vignette.for_slug('donate_landing_bottom'),
            'featuredcampaign': featuredcampaign,
            'sectors': Campaign.objects.filter(
                campaigntype=Campaign.SECTOR).order_by('name'),
            'featuredprojects': featuredprojects,
            'projects': projects,
        })


def donate_project(request, slug):
    """A profile for each project. Also includes a donation form"""
    project = get_object_or_404(
        Project.published_objects.select_related(
            'volunteerpicture', 'featured_image', 'account', 'overflow'),
        slug=slug)
    if request.method == 'POST':
        # only relevant during validation
        if project.account.funded():
            project_max = None
        else:
            project_max = project.account.remaining()
        form = DonationAmountForm(data=request.POST, project_max=project_max)
        if form.is_valid():
            if project.account.funded() and project.overflow:
                code = project.overflow.code
            else:
                code = project.account.code
            params = {'project': code,
                      # convert back into cents
                      'amount': int(form.cleaned_data['payment_amount'] * 100)}
            return HttpResponseRedirect(
                reverse('donations_payment') + '?' + urlencode(params))
    else:
        form = DonationAmountForm()

    return render(
        request,
        'donations/donate_project.jinja',
        {
            'title': project.title,
            'project': project,
            'account': project.account,
            'donate_form': form,
            "IS_PROJECT": project.account.category == Account.PROJECT,
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
            'projects': projects,
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
            "IS_PROJECT": campaign.account.category == Account.PROJECT,
        })


@csrf_exempt
def failure(request, slug, redirect_to):
    return HttpResponseRedirect(reverse(redirect_to, kwargs={'slug': slug})
                                + '?payment_status=failed')


class AbstractReturn(DetailView):
    """Shared by views related to users returning from pay.gov. This includes
    success pages for projects/funds"""
    def post(self, request, *args, **kwargs):
        path = request.path
        params = request.GET.urlencode()
        if params:
            path += "?" + params
        return HttpResponseRedirect(path)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(AbstractReturn, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Must add sharing link info"""
        context = super(AbstractReturn, self).get_context_data(**kwargs)
        path = self.request.scheme + "://" + self.request.get_host()
        path += reverse("donate " +
                        self.get_context_object_name(context['object']),
                        kwargs={'slug': context['object'].slug})
        context['share_url'] = path
        context['share_text'] = settings.SHARE_TEMPLATE % path
        context['share_subject'] = settings.SHARE_SUBJECT
        return context


class ProjectReturn(AbstractReturn):
    queryset = Project.objects.select_related(
        'account', 'country', 'featured_image', 'overflow',
        'volunteerpicture')


class CampaignReturn(AbstractReturn):
    queryset = Campaign.objects.select_related('account', 'featured_image')


class FAQs(ListView):
    model = FAQ
    template_name = 'donations/faq.jinja'
