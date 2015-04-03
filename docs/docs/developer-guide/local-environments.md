<h1>Running a Local Environment</h1>

In this section:

[TOC]

<hr>

## Prerequisites

- Install `Vagrant`, a tool used to manage virtual machines on your computer. You can download Vagrant from https://www.vagrantup.com/.
- `Fork` and `clone` the `18F/peacecorps-site` repository locally on your computer. If you've forked the repository to a personal account (`janedoe`), you can accomplish this with the following `bash` command:

```bash
$ git clone git@github.com:janedoe/peacecorps-site.git
```

## Running Vagrant
In your command line, from the `peacecorps-site` directory, start vagrant:

```bash
$ vagrant up
```

This will start a virtual machine and provision the django site. If you'd prefer to do this on your own, you can see what happens in the [shell script](https://github.com/18F/peacecorps-site/blob/master/provision/dev/bootstrap.sh).

Once the initalization has finished, ssh in to the machine and start up Django's runserver:

```bash
$ vagrant ssh
$ python manage.py runserver 0.0.0.0:8000
```

You can then access the site from your web browser by going to http://192.168.19.61:8000

The setup script also creates an initial superuser for you. You can access the Django admin page at http://localhost:8000/admin and the username and password are provided below:

- Username: `testuser@peacecorps.gov`
- Password: `0QDOyB!gfKkY23$UspzDM35%`

## Running Additional Django Commands
If you wish to run additional vagrant commands (like migrations), SSH in to the Vagrant virtual machine (`vagrant ssh`) and then run them like normal. For instance:

```bash
$ vagrant ssh
$ python manage.py makemigrations
```

Or, to run tests:

```bash
$ python manage.py test --settings=peacecorps.settings.test
```

## CSS and Javascript Development
The project uses [SASS](http://sass-lang.com/) to compile SCSS to CSS, and [Grunt](http://gruntjs.com/) to build static dependencies. Static files are located in the `peacecorps/peacecorps/static/peacecorps` folder ([quicklink](https://github.com/18F/peacecorps-site/tree/master/peacecorps/peacecorps/static/peacecorps) to GitHub). When editing `CSS` and `JS`, it is important to make all edits in the requisite `css/src/` or  `js/src/` folders to ensure changes are not overwritten.

### Running Grunt
In order to compile all static assets, you can run the following commands:

```bash
$ vagrant ssh
$ cd /vagrant/peacecorps/peacecorps/static/peacecorps
$ grunt build
```

To make it easier, Grunt can be configured to watch files and automatically update, so that you don't have to run `grunt build` on each change:

```bash
$ grunt build-watch
```

## Styleguide
Grunt also automatically generates a [Styleguide](https://rawgit.com/18F/peacecorps-site/master/peacecorps/peacecorps/static/peacecorps/resources/styleguide/section-base.html) from all static assets.