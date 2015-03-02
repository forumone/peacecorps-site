# @todo split into smaller files; remove "donate_" prefix
from collections import defaultdict
from urllib.parse import quote as urlquote

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_exempt

from peacecorps.forms import DonationAmountForm, DonationPaymentForm
from peacecorps.models import (
    Account, Campaign, FAQ, FeaturedCampaign, FeaturedProjectFrontPage,
    Issue, Project)
from peacecorps.payxml import convert_to_paygov


def project_form(request, slug):
    """Wrapper around donation_payment which passes in the correct project"""
    project = get_object_or_404(
        Project.published_objects.select_related(
            'volunteerpicture', 'featured_image', 'account', 'overflow'),
        slug=slug)
    account = project.account
    if account.funded() and project.overflow:
        if project.overflow.category == Account.PROJECT:
            path_name = 'donate project'
        else:
            path_name = 'donate campaign'
        return HttpResponseRedirect(
            reverse(path_name,
                    kwargs={'slug': project.overflow.project_or_fund().slug})
            + '?payment_status=full')
    else:
        return donation_payment(request, account, project=project)


def campaign_form(request, slug):
    """Wrapper around donation_payment which passes in the correct campaign"""
    campaign = get_object_or_404(
        Campaign.published_objects.select_related('account'), slug=slug)
    return donation_payment(request, campaign.account, campaign=campaign)


def donation_payment(request, account, project=None, campaign=None):
    """Collect donor contact information. Expects a GET param, payment_amount,
    in dollars."""
    form = DonationAmountForm(data=request.GET, account=account)
    if not form.is_valid():
        if project:
            url = reverse('donate project', kwargs={'slug': project.slug})
        else:
            url = reverse('donate campaign', kwargs={'slug': campaign.slug})
        return HttpResponseRedirect(
            url + '?payment_amount='
            + urlquote(request.GET.get('payment_amount', ''))
            + '&nonce=' + get_random_string(12) + '#amount-form')
    # convert to cents
    payment_amount = int(form.cleaned_data['payment_amount'] * 100)

    context = {
        'title': 'Giving Checkout',
        'payment_amount': payment_amount,
        'project': project,
        'campaign': campaign,
        'agency_id': settings.PAY_GOV_AGENCY_ID,
        'app_name': settings.PAY_GOV_APP_NAME,
        'oci_servlet_url': settings.PAY_GOV_OCI_URL,
    }

    if request.method == 'POST':
        form = DonationPaymentForm(request.POST)
    else:
        form = DonationPaymentForm()
    context['form'] = form

    if project:
        context['ajax_url'] = reverse('api:project_payment',
                                      kwargs={'slug': project.slug})
    else:
        context['ajax_url'] = reverse('api:fund_payment',
                                      kwargs={'slug': campaign.slug})

    if form.is_valid() and request.POST.get('force_form') != 'true':
        data = {k: v for k, v in form.cleaned_data.items()}
        data['payment_amount'] = payment_amount
        data['project_code'] = account.code
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

    featuredcampaign = FeaturedCampaign.objects.filter(pk=1).first()

    return render(
        request,
        'donations/landing.jinja',
        {
            'title': 'Donate',
            'featuredcampaign': featuredcampaign,
            'sectors': Campaign.published_objects.filter(
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

    if 'payment_amount' in request.GET:
        form = DonationAmountForm(data=request.GET, account=project.account)
    else:
        form = DonationAmountForm(account=project.account)

    return render(
        request,
        'donations/donate_project.jinja',
        {
            'title': project.title,
            'project': project,
            'account': project.account,
            'donate_form': form,
            "PROJECT": Account.PROJECT
        })


def donate_projects_funds(request):
    """
    The page that displays a sorter for all projects, issues, volunteers.
    """
    # @todo - hide some of the prefetching logic?
    country_funds = Campaign.published_objects.prefetch_related('country')
    country_funds = country_funds.filter(campaigntype=Campaign.COUNTRY)
    country_funds = country_funds.order_by('country__name')

    issues = Issue.objects.prefetch_related('campaigns').order_by('name')
    projects = Project.published_objects.prefetch_related(
        Prefetch('account', queryset=Account.objects.all()),
        'campaigns',
        'country',
        'volunteerpicture'
    ).order_by('volunteername')
    # Before we can build projects_by_issue, we need to know which funds are
    # associated with which issues
    issues_by_campaign = defaultdict(list)
    for issue in issues:
        for campaign in issue.campaigns.all():
            issues_by_campaign[campaign.id].append(issue.id)

    projects_by_issue = defaultdict(int)
    projects_by_country = defaultdict(int)
    # This will be used to indicate which issues a project is a part of
    project_filters = {}
    for project in projects:
        projects_by_country[project.country.code] += 1
        project_filters[project.id] = 'country-' + project.country.code
        for campaign in project.campaigns.all():
            for issue_id in issues_by_campaign[campaign.id]:
                project_filters[project.id] += ",issue-" + str(issue_id)
                projects_by_issue[issue_id] += 1

    return render(
        request,
        'donations/all.jinja',
        {
            'title': 'Projects and Funds',
            'country_funds': country_funds,
            'issues': issues,
            'projects': projects,
            'projects_by_country': projects_by_country,
            'projects_by_issue': projects_by_issue,
            'project_filters': project_filters,
        })


def memorial_funds(request):
    """Contains memorial funds"""
    memorial_funds = Campaign.published_objects.filter(
        campaigntype=Campaign.MEMORIAL)
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
    return render(request, "donations/memorial_funds.jinja", {
        "memorial_funds": memorial_funds,
        'title': 'Memorial Funds'})


def fund_detail(request, slug):
    campaign = get_object_or_404(
        Campaign.published_objects.select_related('account'), slug=slug)
    if 'payment_amount' in request.GET:
        form = DonationAmountForm(data=request.GET, account=campaign.account)
    else:
        form = DonationAmountForm(account=campaign.account)

    return render(
        request,
        'donations/fund_detail.jinja',
        {
            'title': 'Donate',
            'campaign': campaign,
            'account': campaign.account,
            'donate_form': form,
            "PROJECT": Account.PROJECT
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
        context['share_text'] = settings.SHARE_TEMPLATE
        context['share_subject'] = settings.SHARE_SUBJECT
        context['share_tweet'] = settings.SHARE_TWEET
        context['title'] = 'Thank You'
        return context


class ProjectReturn(AbstractReturn):
    queryset = Project.objects.select_related(
        'account', 'country', 'featured_image', 'overflow',
        'volunteerpicture')


class CampaignReturn(AbstractReturn):
    queryset = Campaign.published_objects.select_related(
        'account', 'featured_image')


class FAQs(ListView):
    model = FAQ
    template_name = 'donations/faq.jinja'

    def get_context_data(self, **kwargs):
        """Add title"""
        context = super(FAQs, self).get_context_data(**kwargs)
        context['title'] = 'Donating FAQs'
        return context


def four_oh_four(request):
    return render(request, '404.jinja', {'title': 'Page Not Found'},
                  status=404)
