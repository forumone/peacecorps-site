<h1>Deployment</h1>

In this section:

[TOC]

<hr>

This section details major dependencies and software packages used:

## Django

See [requirements.txt](https://github.com/Threespot/peacecorps-site/blob/master/requirements.txt) for packages required by Django for the application to function. Note that there are several packages that rely on forks or specific patches from the upstream git repository, thus access to both the [Python Package Index](https://pypi.python.org) and [GitHub](https://github.com) is required.

See [requirements-dev.txt](https://github.com/Threespot/peacecorps-site/blob/master/requirements-dev.txt) for additional requirements needed in local development environments. The Vagrant provisioner automatically takes care of this for you.

## Servers
All servers are based off [FISMA Ready Ubuntu 14.04 LTS](https://github.com/fisma-ready/ubuntu-lts). Packer, when used in local development, will use a base AMI from AWS then use shell scripts to bring the AMI up to the FISMA Ready baseline. The following packages are used on _all_ deployed servers:

```
fail2ban
git
build-essential
python-pip
boto
awscli
```

### NAT Instances
The following packages are installed on servers acting as a NAT:

```
nginx
```

### Web Server Instances
The following packages are installed on servers acting as Web Servers (either public or paygov):

```
nginx
openssl
libssl-dev
python-dev
libevent-dev
libpq-dev
python-virtualenv
postgresql-client-common
postgresql-client
libmemcached-dev
libbz2-dev
libsqlite3-dev
libreadline-dev
libjpeg-dev
zlib1g-dev
libtiff5-dev
sendmail
pyenv
python 3.4.1
```
