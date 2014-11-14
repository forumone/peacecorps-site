import csv
from datetime import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from peacecorps.models import Campaign, Country, Account, Project


def datetime_from(text):
    """Convert a string representation of a datetime into a UTC datetime
    object."""
    # This format will no doubt change
    return timezone.make_aware(datetime.strptime(text, "%Y-%m-%d %H:%M:%S"),
                               timezone.get_current_timezone())


def cents_from(text):
    """Convert a string of comma-separated dollars and decimal cents into an
    int of cents"""
    text = text.replace(",", "").strip()
    #   intentionally allow errors to break the script
    dollars = float(text)
    return int(round(dollars * 100))


def find_issue(sector_name):
    """Map sector names to their appropriate issue; text is not always an
    exact match"""
    name_mismatch = {
        'Health and HIV/AIDS': 'Health', 'IT': 'Technology',
        'Water and Sanitation': 'Drinking Water and Sanitation',
        'Youth Development': 'Youth'}
    campaign_name = name_mismatch.get(sector_name, sector_name)
    return Campaign.objects.filter(name=campaign_name).first()


def create_account_pcpp(row):
    """This is a new project. Create the associated account information and
    generate an empty Project"""
    try:
        country = Country.objects.get(name__iexact=row['COUNTY_NAME'])
        issue = find_issue(row['SECTOR'])
        goal = cents_from(row['PROJ_REQUEST'])
        balance = cents_from(row['PROJ_BAL'])
        account = Account.objects.create(
            name=row['PROJ_NAME'], code=row['PROJ_CODE'],
            current=(goal - balance), goal=goal, category=Account.PROJECT,
            community_contribution=cents_from(row['COMM_CONTRIB']))
        volunteername = row['PCV_NAME']
        if volunteername.startswith(row['STATE']):
            volunteername = volunteername[len(row['STATE']):].strip()
        project = Project.objects.create(
            title=row['PROJ_NAME'], country=country, account=account,
            overflow=issue.account, volunteername=volunteername,
            volunteerhomestate=row['STATE'], description=row['SUMMARY']
        )
        project.campaigns.add(issue)
    except ObjectDoesNotExist:
        logging.warning("Either country or issue does not exist: %s, %s",
                        row['COUNTY_NAME'], row['SECTOR'])


def update_account(row, account):
    """If an account already exists, synchronize the transactions and amount"""
    updated_at = datetime_from(row['LAST_UPDATED_FROM_PAYGOV'])
    account.donations.filter(time__lte=updated_at).delete()
    account.current = cents_from(row['REVENUE'])
    account.save()


class Command(BaseCommand):
    help = """Synchronize Account and Transactions with a CSV.
              Generally, this means deleting transactions and updating the
              amount field in the account."""

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError("Missing path to csv")

        with open(args[0], encoding='iso-8859-1') as csvfile:
            # Column names will no doubt change
            for row in csv.DictReader(csvfile):
                account = Account.objects.filter(
                    code=row['PROJ_CODE']).first()
                if account:
                    update_account(row, account)
                else:
                    create_account_pcpp(row, account)
