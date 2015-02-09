peacecorps-site
===============

A place to think and work on a new Peace Corps website.

## Setup

This is a Django application that depends on Python 3.

### Installing Python 3
There are multiple approaches to installing Python 3, depending on your personal setup and preferences.

One option is to [pyenv](https://github.com/yyuu/pyenv) to manage downloading Python 3 or you can install them directly.

For OS X, install Homebrew](http://brew.sh) (OS X), then run `brew install Python3`. For Ubuntu, install using `apt-get install Python3`.


### Project setup

Create an environment to install Python dependencies, with virtualenvwrapper.

```bash
mkvirtualenv --python=/path/to/python3 peacecorps-site
```

Example:
```bash
mkvirtualenv --python=/usr/local/bin/python3 peacecorps-site
```

Note: You don't need to explicitly specify the Python version, especially if
you use pyenv + virtualenvwrapper. Running mkvirtualenv in that scenario will
'freeze' the currently active version of Python.

Pull down the repo:

```bash
git clone https://github.com/18F/peacecorps-site
cd peacecorps-site
```

Install project requirements:

```bash
pip install -r requirements.txt
```

If you are in a development environment, you might want some of the development
tools:

```bash
pip install -r requirements-dev.txt
```

### Settings

You will also need to create a `local_settings.py` file inside
peacecorps/settings.  It should contain `SECRET_KEY` and `DATABASES`
configurations. Up-and-running defaults (using sqlite) can be found in the
test.py configuration.  See the Django settings
[documentation](https://docs.djangoproject.com/dev/ref/django-admin/) for
details. 

### Loading Data

To synchronize to the latest schema, change into the `peacecorps` directory
and then run:
```bash
python manage.py migrate
```

Next, you will want to load fixtures related to countries, issues, and special
funds:

```bash
python manage.py loaddata countries; python manage.py loaddata issues; python manage.py loaddata global-general
```

Now the database will contain a list of countries, several issues (and their
associated sector funds) as well as the General Fund and the Global Fund.

You will want to synchronize with the latest account export:

```bash
python manage.py sync_accounting /path/to/file.csv
```

After this, your database should include many projects, but none will be
"published". A simple fix is to "publish" all projects which have not met
their goal.

```bash
python manage.py dbshell
    update peacecorps_project set published=1 where account_id in (select id from peacecorps_account where goal > current);
```


### Front end development
See [front end development](/peacecorps/peacecorps/static/peacecorps/README.md) 
