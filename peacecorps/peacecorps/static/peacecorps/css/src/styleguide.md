# Peace Corps Styleguide

## Overview

This is an automatically generated style guide for the Peace Corps site. This
styleguide system parses comments in the sites sass files and generates this
markup to be displayed as a guide. The guide is generated with the tool
node-kss.

When new css styling is added to the site, it should be documented according
to the KSS standards. If everything is documented correctly, it will appear in
this style guide when the build is run.

This guide can be used as a reference to use the CSS system as well as a testing
environment for visuals of the site.

## Contents
##### [base](section-base.html)
##### [components](section-components.html)
##### [modules](section-modules.html)

## Setup
This styleguide was setup with [KSS node](https://github.com/kss-node/kss-node).
To integrate it into your project, here are some simple instructions:

```bash
npm install --save-dev kss
kss-node --init /path/to/custom_template
kss-node /path/to/sass /path/to/styleguide --template /path/to/custom_template
## Edit the /path/to/sass/styleguide.md file to your liking.
## Modify the /path/to/custom_template/public files to your liking.
```

KSS will only process comments in sass files that adhere to its format. More
about the format can be found on the [kss
site](http://warpspire.com/kss/syntax/)
