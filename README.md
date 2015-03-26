peacecorps-site
===============

A place to think and work on a new Peace Corps website.

## Setup

This is a Django application that depends on Python 3. For easy of use, we've included a `Vagrantfile` that will get you up and running in a nice, easy to use development environment.

### Installing Vagrant
Download and install Vagrant from https://www.vagrantup.com/


### Get Started
From the project directory, start up Vagrant:

```bash
$ vagrant up
```

This will kick off a process to provision and set up a development environment for you. If you'd prefer to do this on your own, you can see what happens in `provision/dev/bootstrap.sh`.

Once the initalization has finished, ssh in to the machine and start up Django's runserver:

```bash
$ vagrant ssh
$ python manage.py runserver 0.0.0.0:8000
```

You can then access the site from your web browser by going to http://localhost:8000

The setup script also creates an initial superuser for you. You can access the Django admin page at http://localhost:8000/admin and the username and password are provided below:

Username: `testuser@peacecorps.gov`
Password: `0QDOyB!gfKkY23$UspzDM35%`

### Running Additional Django Commands
If you wish to run additional vagrant commands (like migrations), SSH in to the Vagrant virtual machine (`vagrant ssh`) and then run them like normal. For instance:

```bash
$ vagrant ssh
$ python manage.py makemigrations
```

### Front end development
See [front end development](/peacecorps/peacecorps/static/peacecorps/README.md) 
