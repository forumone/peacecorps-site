#!/usr/bin/env bash

sudo apt-get update -y
sudo apt-get install python-pip -y
sudo apt-get install git -y

sudo apt-get install libevent-dev -y
sudo apt-get install libpq-dev -y
sudo apt-get install libtiff4-dev -y
sudo apt-get install libjpeg8-dev -y
sudo apt-get install zlib1g-dev -y
sudo apt-get install libmemcached-dev -y
sudo apt-get install python-virtualenv -y
sudo apt-get install python-dev -y
sudo apt-get install libbz2-dev -y
sudo apt-get install libsqlite3-dev -y
sudo apt-get install libreadline-dev -y
sudo apt-get install -y build-essential

curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -
sudo apt-get install nodejs -y
sudo apt-get install npm -y
sudo npm install -g grunt-cli



sudo su vagrant <<'EOF'
export USE_HTTPS=True
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
. ~/.bash_profile
pyenv install 3.4.1
pyenv rehash
pyenv virtualenv 3.4.1 peacecorps
pyenv rehash
pyenv activate peacecorps
pip install -r /vagrant/requirements.txt
pip install -r /vagrant/requirements-dev.txt
cd /vagrant/peacecorps
python manage.py migrate
python manage.py loaddata countries issues global-general
python manage.py loaddata /vagrant/provision/dev/testuser.json
python manage.py sync_accounting /vagrant/provision/dev/fund_data.csv
cat /vagrant/provision/dev/publish_cy15_projects.py | python manage.py shell
echo 'cd /vagrant/peacecorps' >> ~/.bash_profile
echo 'pyenv activate peacecorps' >> ~/.bash_profile
cd /vagrant/peacecorps/peacecorps/static/peacecorps
npm install
rm -rf node_modules
npm install
EOF