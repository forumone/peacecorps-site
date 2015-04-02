<h1>Pay.gov Connection</h1>

In this section:

[TOC]

<hr>

The site connects to Pay.gov through an interactive API that is limited to requests coming from Pay.gov.

## Connection Steps
When a user initiates a transaction:

1. They first provide some initial information (Name, Address, Amount to Contribute) on a form ([example](https://beta.peacecorps.gov/donate/fund/let-girls-learn/payment/?payment_amount=50)).
2. Upon hitting `CONTINUE TO PAY.GOV`, Django issues a `POST` request to pay.gov with the submitted data and receives a unique `agency_tracking_id` to identify the transaction.
3. Django then sends the user directly to pay.gov to finish the transaction. If the user has javascript enabled, this is invisible (they are redirected automatically after submitting the initial form). If the user does not have javascript enabled, they must click an additional button to be redirected.
4. The user enters their payment information and confirms on pay.gov.
5. pay.gov sends a `POST` request to Django with the `agency_tracking_id` and either `SUCCESS` or `FAILURE`.
5. pay.gov redirects the user back to Django, where Django displays either a SUCCESS or FAILURE message.

## Referenced Code
On pay.gov servers, the environmental variable `USE_PAYGOV=True` enables pay.gov functionality in Django. This installes the `paygov` django app. In [production settings](https://github.com/18F/peacecorps-site/blob/master/peacecorps/peacecorps/settings/production.py#L44-L45):

```
if os.environ.get('USE_PAYGOV', ''):
    INSTALLED_APPS += ('paygov',)
```

Code and tests around paygov intergration can be found on [GitHub](https://github.com/18F/peacecorps-site/tree/master/peacecorps/paygov).