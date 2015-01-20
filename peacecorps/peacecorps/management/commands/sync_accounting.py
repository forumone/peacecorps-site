import csv
import json
from datetime import datetime
import logging
import re

from django.core.management.base import BaseCommand, CommandError
import pytz

from peacecorps.models import (
    Account, Campaign, Country, Project, SectorMapping)


def datetime_from(text):
    """Convert a string representation of a date into a UTC datetime. We
    assume the incoming date is in Eastern and represents the last second of
    that day. We must account for a misleading timestamp; only the date
    provided is relevant"""
    eastern = pytz.timezone("US/Eastern")
    if text.endswith("T00:00:00"):
        text = text[:-len("T00:00:00")]
    time = datetime.strptime(text, "%Y-%m-%d")
    time = time.replace(hour=23, minute=59, second=59)
    time = eastern.localize(time)
    return time.astimezone(pytz.utc)


def cents_from(text):
    """Convert a string of comma-separated dollars and decimal cents into an
    int of cents"""
    text = text.replace(",", "").strip()
    #   intentionally allow errors to break the script
    dollars = float(text)
    return int(round(dollars * 100))


class IssueCache(object):
    """Keeps track of all known issues, so that we do not need to hit the
    database with each request."""

    def __init__(self):
        self.issues = {m.accounting_name: m.campaign
                       for m in SectorMapping.objects.all()}

    def find(self, sector_name):
        if sector_name not in self.issues:
            # may have been added
            mapping = SectorMapping.objects.filter(pk=sector_name).first()
            if mapping:
                self.issues[mapping.accounting_name] = mapping.campaign
        return self.issues.get(sector_name)


def create_account(row, issue_map):
    """This is a new project/campaign. Determine the account type and create
    the appropriate project, country fund, etc."""
    acc_type = account_type(row)
    name = row['PROJ_NAME1']
    if Account.objects.filter(name=name).first():
        name = name + ' (' + row['PROJ_NO'] + ')'
    account = Account(name=name, code=row['PROJ_NO'], category=acc_type)
    if acc_type == Account.PROJECT:
        create_pcpp(account, row, issue_map)
    else:
        create_campaign(account, row, name, acc_type)


def create_campaign(account, row, name, acc_type):
    """Create and save a campaign (and account). Also save sector name mapping
    if creating a sector fund. May error if trying to add a country fund for a
    country which does not exist."""
    country = None
    if acc_type == Account.COUNTRY:
        country_name = row['LOCATION']
        country = Country.objects.filter(name__iexact=country_name).first()
        if not country:
            logging.getLogger('peacecorps.sync_accounting').warning(
                "Country does not exist: %s", row['LOCATION'])
            return

    account.save()
    summary = clean_description(row['SUMMARY'])
    campaign = Campaign.objects.create(
        name=name, account=account, campaigntype=acc_type,
        description=json.dumps({"data": [{"type": "text",
                                          "data": {"text": summary}}]}),
        country=country)
    if acc_type == Account.SECTOR:
        # Make sure we remember the sector this is marked as
        SectorMapping.objects.create(pk=row['SECTOR'], campaign=campaign)


def create_pcpp(account, row, issue_map):
    """Create and save a project (and account). This is a bit more complex for
    projects, which have goal amounts, etc."""
    country_name = row['LOCATION']
    country = Country.objects.filter(name__iexact=country_name).first()
    issue = issue_map.find(row['SECTOR'])
    if not country or not issue:
        logging.getLogger('peacecorps.sync_accounting').warning(
            "Either country or issue does not exist: %s, %s",
            row['LOCATION'], row['SECTOR'])
    else:
        goal = cents_from(row['PROJ_REQ'])
        balance = cents_from(row['UNIDENT_BAL'])
        account.current = goal - balance
        account.goal = goal
        account.community_contribution = cents_from(row['OVERS_PART'] or '0')
        account.save()

        volunteername = row['PCV_NAME']
        if volunteername.startswith(row['STATE']):
            volunteername = volunteername[len(row['STATE']):].strip()

        summary = clean_description(row['SUMMARY'])
        sirtrevorobj = {"data": [{"type": "text", "data": {"text": summary}}]}
        description = json.dumps(sirtrevorobj)

        project = Project.objects.create(
            title=row['PROJ_NAME1'], country=country, account=account,
            overflow=issue.account, volunteername=volunteername,
            volunteerhomestate=row['STATE'], description=description
        )
        project.campaigns.add(issue)


def update_account(row, account):
    """If an account already exists, synchronize the transactions and amount"""
    if row['LAST_UPDATED_FROM_PAYGOV']:
        updated_at = datetime_from(row['LAST_UPDATED_FROM_PAYGOV'])
        account.donations.filter(time__lte=updated_at).delete()
    if account.category == Account.PROJECT:
        goal = cents_from(row['PROJ_REQ'])
        balance = cents_from(row['UNIDENT_BAL'])
        account.current = goal - balance
        account.save()


def account_type(row):
    """Derive whether this account is a project, country fund, etc. by
    heuristics on the project code, sector, and other fields"""
    if row['PROJ_NO'].endswith('-CFD') or (
            row['SECTOR'] == 'None' and row['PROJ_REQ'] == '0'
            and row['PCV_NAME'] == row['LOCATION'] + ' COUNTRY FUND'):
        return Account.COUNTRY
    if (row['PROJ_NO'].startswith('SPF-')
            and 'MEMORIAL' in row['PROJ_NAME1'].upper()):
        return Account.MEMORIAL
    if row['PROJ_NO'].startswith('SPF-') and (
            row['LOCATION'] == 'D/OSP/GGM'
            or row['PROJ_NAME1'].upper() == row['PCV_NAME'].upper()):
        return Account.SECTOR
    if re.match(r'[\d-]+', row['PROJ_NO']) or row['OVERS_PART']:
        return Account.PROJECT
    return Account.OTHER


def process_rows_in(reader):
    """Run through rows in the CSV file, creating/updating accounts. Delay
    processing of PROJECT accounts until the end (as they may rely on funds
    created later). Note that we accomplish this by effectively storing the
    CSV in memory. This shouldn't be a problem given expected file sizes"""
    project_rows, other_rows = [], []
    for row in reader:
        if account_type(row) == Account.PROJECT:
            project_rows.append(row)
        else:
            other_rows.append(row)

    issue_map = IssueCache()
    logger = logging.getLogger('peacecorps.sync_accounting')
    for row in other_rows + project_rows:
        account = Account.objects.filter(code=row['PROJ_NO']).first()
        if account:
            logger.info(
                'Updating %s, new balance: %s / %s', row['PROJ_NO'],
                row['UNIDENT_BAL'], row['PROJ_REQ'])
            update_account(row, account)
        else:
            logger.info('Creating %s', row['PROJ_NO'])
            create_account(row, issue_map)


def clean_description(text):
    """The original datasource introduces some common, incorrect encodings.
    Fix them here"""
    text = text.replace("\u00c2\u00bf", "'")
    text = re.sub(r"<\s*br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</\s*br>", "", text, flags=re.IGNORECASE)
    return text


class Command(BaseCommand):
    help = """Synchronize Account and Transactions with a CSV.
              Generally, this means deleting transactions and updating the
              amount field in the account."""

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError("Missing path to csv")

        with open(args[0], encoding='iso-8859-1') as csvfile:
            process_rows_in(csv.DictReader(csvfile))
