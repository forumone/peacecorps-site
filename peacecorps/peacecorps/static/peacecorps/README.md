peacecorps-site-frontend
========================

The frontend portion of the peacecorp site, with CSS and JS dependencies.

## Styleguide

[styleguide] (https://rawgit.com/Threespot/peacecorps-site/master/peacecorps/peacecorps/static/peacecorps/resources/styleguide/section-base.html)


## Development
We use nodejs, node-sass, Bourbon, and Neat for our front-end stack.

### Javascript & CSS
#### Install node

##### Mac & Windows
- *For Mac, use Homebrew!*
- Visit http://nodejs.org/download/.
- Click the link for 32-bit .msi instaler for Windows or Universl .pkg for Mac.
- Click the downloaded file.
- Go through the various steps to install.

##### Linux
In a terminal run the following command(s):

```bash
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get install nodejs
sudo apt-get install npm
```

#### Run tests and build
From the peacecorps/peacecorps/static/peacecorps directory, run the following from
the command line:

Installs Node dependencies:
```bash
npm install
```

Run JS tests (note the `npm run` prefix - required because we are *not* installing Grunt globally)

```bash
npm run grunt test
```

Build JS and CSS assets

```bash
npm run grunt build
```

Watch all the JS & CSS files and build when changes have been detected. This will
recompile files immediately as you work on them, easing development.

```bash
npm run grunt build-watch
```
