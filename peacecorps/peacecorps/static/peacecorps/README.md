peacecorps-site-frontend
========================

The frontend portion of the peacecorp site, with CSS and JS dependencies.

## Development
We use nodejs, SASS, Bourbon, and Neat for our front-end stack.

### Sass
To up Sass you will need ruby (and gem) installed. On a Debian/Linux box, this can be
accomplished via:

```bash
sudo apt-get install ruby
```

You next need to install the appropriate ruby libraries. In this example, we
will install them system wide, though you may prefer bundler, etc.

```bash
sudo gem install neat sass bourbon
```

You will then need to pull down the appropriate sass libraries for bourbon and
neat:

```bash
cd peacecorps/peacecorps/static/peacecorps/sass
bourbon install
neat install
```

Finally, run the "watch" script, which will recompile CSS as you make SASS
changes. From within the sass directory:

```bash
sass --watch .:../css
```

### Javascript
#### Install node

##### Mac & Windows
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
From the peacecorp/peacecorp/static/peacecorp directory, run the following from
the command line:

```bash
npm install
```

Run JS tests

```bash
grunt test
```

Build JS assets

```bash
grunt build
```

Watch all the JS files and build when changes have been detected. This will
recompile files immediately as you work on them, easing development.

```bash
grunt buildWatch
```

## Notes
In the future, we will merge the build process so CSS and JS builds are not separate.

