"""Convert an integer quantity of cents into a dollar amount, separated by
commas"""
from django_jinja import library


@library.global_function
def humanize_cents(amount):
    return "${:,.2f}".format(amount/100.0)
