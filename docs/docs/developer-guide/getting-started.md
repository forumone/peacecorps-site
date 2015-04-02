<h1>Getting Started</h1>

Welcome to the new _beta.peacecorps.gov_ developer guide! This documentation is designed to get you up and running with a Django developer environment for the site.

In this section:

[TOC]

<hr>

## Using Git

The first thing you'll need to do is `clone` your personal fork of the Git repository (https://github.com/18f/peacecorps-site) from GitHub. If you are unsure of how to use `git`, here are some resources to get you started:

- [GitHub Guides](https://guides.github.com/) offers a variety of tutorials and articles on using Git and GitHub
- [Git Immersion](http://gitimmersion.com/) offers an in-depth dive in to Git
- [Try Git](https://try.github.io) offers an interactive 15 minute command line tutorial
- [Code School](https://www.codeschool.com/courses/git-real) has a number of Git courses you can take

A complete walk-though of `git` is outside the scope of the documentation, but follows is a brief overview of concepts on how we manage the repository and releases.

## Developer Workflow

- Each developer works off a `fork` of the main [18F Repository](https://github.com/18f/peacecorps-site). These forks are located in their personal GitHub accounts. For instance, here is [Sean Herron's](https://github.com/seanherron/peacecorps-site) and [CM Lubinski's](https://github.com/cmc333333/peacecorps-site).
- Individual Feature Enhancements, bugfixes, or changes are created as `branches` off the main `master` branch. For instance, if a developer is creating a feature that introduces search across the site, they would create a `search` branch of `master` which contains all work specific to search. If they, at the same time, needed to fix a bug unrelated to search (perhaps around font sizes), they would `commit` their work in `search`, switch back to `master`, and create a new `fix_font_size` branch with that specific bugfix. The goal is to scope each branch to a specific item of work, and not bundle too many things together.
- When work on a branch is complete, the developer would create a `Pull Request` on the main `18f/peacecorps-site` repository to propose merging the branch in to the main `master` release. [Here](https://github.com/18F/peacecorps-site/pull/317) is an example Pull Request, with discussion.
- A second developer would then review the Pull Request to ensure it passes all required automated tests, uses best practices, and makes sense. They would then `merge` the branch or ask the first developer to make changes as a precursor to merging.

## Releases

From the `master` branch, the code is packaged in releases that align with [Semantic Versioning](http://semver.org/). In order to deploy to either the staging or production environment, code must be put in to a release. Current releases may be found at https://github.com/18F/peacecorps-site/releases.

### Creating a New Release
To create a new release, click "Draft a New Release" at https://github.com/18F/peacecorps-site/releases. Provide the release number for both the _tag version_ and _release title_. Semantic Versioning defines the following structure for version names:

Given a version number `MAJOR.MINOR.PATCH`, increment the:

- `MAJOR` version when you make incompatible API changes,
- `MINOR` version when you add functionality in a backwards-compatible manner, and
- `PATCH` version when you make backwards-compatible bug fixes.

Thus, if the current release is `1.4.6`, the above mentioned font bug fix would increment the version to `1.4.7`, and the search feature enhancement would increment the version to `1.5.0`. This can continue indefinitely (eg. `1.241.888` is a valid version). A change that introduces backwards incompatible changes would reset the major version (eg. `2.0.0`).

## A note on Tests
Test creation and coverage is an important part of the development process. We use [CircleCI](https://circleci.com/gh/18F/peacecorps-site) and an extensive Django and Javascript test suite to ensure appropriate code behavior. New Pull Requests should always include full test coverage.