<h1>PCPP Projects & Funds</h1>
In this section:

[TOC]

<hr>


Projects and Fund data is imported from Odyssey (Peace Corps' internal financial management system) on a regular basis. The details of how this import works are fairly complex, but at a high level, here's how things work:

- Approximately once per hour, Odyssey sends the CMS a file that contains a number of details about every project and fund it knows about.
- Using the information in that file, we look through every project and fund and place it in to one of two buckets:
1. If the project or fund is _new_ and has not been seen by the system before, we create an `account` and a `campaign` or `project` entry for the corresponding accounting code.
2. If the project or fund has been _previously seen_, we update a few pieces of financial information, but otherwise discard it.

It's important to remember this simple distinction between the role of Odyssey and the role of the CMS: Odyssey is used primarily to provide _financial information_ to the system, while the CMS is used to provide _content and contextual information_ about the project or fund.

## Accounts, Projects, and Campaigns
Within the CMS, there are three concepts relating to items imported from Odyssey: `Accounts`, `Projects`, and `Campaigns`. Each item has a corresponding `Account`, and depending on the nature of the item also has either a `Project` or `Campaign` associated with it.

### Accounts
![Account Screen](images/accounts.png)

The `Account` entry contains information on the _financial status_ of the project or fund, such as the current monetary amount collected, the goal, and the community contribution. _Everything in this entry is overwritten by Odyssey updates_. Only in extreme circumstances should anything in the `account` entry be touched, and it should always be done in coordination with a developer.

### Projects and Campaigns
The other entry that is automatically created depends on the type of account. PCPP Projects receive an entry in `Projects`, and everything else (eg. Memorial Funds, Country Funds, Sector Funds, etc) receive an entry in `Campaigns`. 

Data within `Projects` and `Campaigns` is _initially populated_ by data from Odyssey, but any changes after the initial population will not be transferred from Odyssey to the CMS. You'll need to make all edits in `Projects` and `Campaigns` within the CMS in order for them to take effect.

For more information, see [Creating a New PCPP Project](#creatingediting-pcpp-projects) and [Creating a New PCPP Campaign](#creatingediting-pcpp-campaigns).

## Issues

Campaigns and Projects also may belong to an "Issue". An issue is a broad categorization of themes, for instance, "Agriculture", "Health", or "Education". They don't need to map to specific sectors, however, each project or campaign **must** belong to at least one issue. Issues are primarily used in the sorter to help with project navigation:

![Issue Sorter](images/issue_sorter.png)

See [Creating or Editing Issues](https://github.com/18F/peacecorps-site/wiki/Creating-or-Editing-Issues) for more information on Issue management.

### How Projects Relate to Issues
Rather than directly associating a `Project` to an `Issue`, a number of Sector `Campaigns` are associated to an `Issue`, and then projects linked to that `Campaign` are associated with the `Issue` automatically.

### Creating or Editing Issues
To create or edit an Issue, select `Issues` from the CMS main page. You can either click on a issue name, or click "Add Issue" in the upper right to add a new issue.
![Issues](images/issues.png)

Clicking on an issue will bring you to the "Change Issue" page. As you can see in this example, we're editing the "Health" issue, which contains two underlying Peace Corps sectors - the "Health and HIV/AIDS" sector and the "Stomping out Malaria in Africa" sector.

![Change Issue](images/change_issue.png)

You can provide a number of information items:

- **Name**: The name of the Issue
- **Icon**: An SVG vector file for an icon to represent the issue. Here's an example of the code in the file used for Health (health.svg):
```

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="80px" height="80px" viewBox="-11 -14 80 80" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">
    <!-- Generator: Sketch 3.2.1 (9977) - http://www.bohemiancoding.com/sketch -->
    <title>icon-health</title>
    <desc>Created with Sketch.</desc>
    <defs></defs>
    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">
        <g id="icon-health" sketch:type="MSLayerGroup" fill="#FFFFFF">
            <path d="M29,51.1 C39,51.1 57.8,30.7 57.8,16.1 C57.8,1.5 40.4,-5.3 29,8.1 C17.7,-5.3 0.2,1.5 0.2,16.1 C0.3,30.7 19,51.1 29,51.1 L29,51.1 Z" id="Shape" sketch:type="MSShapeGroup"></path>
        </g>
    </g>
</svg>
```
- **Icon Background**: The _background_ image that should be used behind the SVG icon. This should be 237px by 237px. When used together with the Icon SVG, it will render on the site like this:

![Issue Icon](images/issue_icon.png) 

- **Campaigns**: An assortment of Sectors to associate with this Issue. Items on the left represent all potential Sectors that could be potentially associated, items on the right represent those that are chosen. You can select a sector and use the left/right arrow icons in the middle to move between the two.

## PCPP Projects & Campaigns

### Creating/Editing PCPP Projects
In this example, we'll walk through the steps needed to make a **new** PCPP Project appear on the website.

1. Create the PCPP Project inside Odyssey, using the existing process.
2. Oddysey will provide an update to the CMS within the hour with the new project data.
3. Once this happens, two new entries will appear in the CMS, one in `Accounts` and in either `Projects`.
4. Open the `Projects` page and find it in the list. You can search by Account Number or Project Title in the search bar at the top.

![Projects Page](images/projects.png)

Once you find the relevant project, click on the account number to be taken to the Change Project page:
![Change Project Page](images/change_project.png)

On this page, you'll see a number of fields, many of which are pre-populated by Odyssey:

#### Account Info
![Account Info](images/account_info.png)

- **Account**: Pre-populated from Odyssey, represents the account number of the project
- **Overflow**: The account donations should be sent to once the project's maximum funding is reached. Defaults to the project's sector.
- **Country**: Prepopulated from Odyssey, represents the country the project occurs in.
- **Funded Status**: Shows if the project has been fully funded or can still accept contributions.

#### Volunteer Info
![Volunteer Info](images/volunteer_info.png)

- **Volunteer Name**: Pre-populated from Odyssey, contains the last name and first initial of the Volunteer.
- **Volunteer Home State**: Pre-populated from Odyssey, contains the US State the Volunteer comes from.
- **Volunteer Picture**: Optional photo of the Volunteer. When provided, it will show up next to their name throughout the site. If no picture is provided, an alternate (such as a map of the country they are serving in) is shown. Uploaded images should be **175px by 175px**. For instructions on uploading a photo, see [Uploading Media](media.md#uploading-media).
![Volunteer Picture](images/volunteer_picture.png)

#### Media
![Project Media Admin](images/project_media.png)

- **Featured Image**: This is the image that appears at the top of the Project's page. If no picture is provided, a default alternate is shown. Uploaded images should be **1100px wide by 454px tall**. For instructions on uploading a photo, see see [Uploading Media](media.md#uploading-media).

#### Project Info
![Project Info Page](images/project_info.png)

- **Title**: The title of the project, imported from Odyssey
- **Tagline**: A shorter title, specifically used in areas where the full title may not work well. If the project is featured, this is used as the title on the homepage.
- **Slug**: Automatically generated from the Title, this will be the URL of the project page. It is suggested to not edit this.
- **Description**: The description is automatically imported from Odyssey, and uses a simple editor to provide rich text and imagery. For more on the functionality of the Description field, see [Rich Content Editing](media.md#rich-content-editing).
- **Abstract**: A shorter version of the description, max of 255 characters.
- **Published**: By default this is "off". Checking the published button makes the project visible on the website.  

Click `Save` and the project will be live on the website, assuming `Published` has been selected.

### Creating/Editing PCPP Campaigns
In this example, we'll walk through the steps needed to make a **new** PCPP Campaign appear on the website. A campaign is anything that is _not_ a project. For instance, Country Funds, Sector Funds, and the Peace Corps Fund are all campaigns.

1. Create the PCPP Campaign inside Odyssey, using the existing process.
2. Oddysey will provide an update to the CMS within the hour with the new campaign data.
3. Once this happens, two new entries will appear in the CMS, one in `Accounts` and in either `Campaigns`.
4. Open the `Campaigns` page and find it in the list. You can search by Account Number or Campaign Title in the search bar at the top.

![Campaigns Page](images/campaigns.png)

Once you find the relevant campaign, click on the account number to be taken to the Change Campaign page:
![Change Campaign Page](images/change_campaign.png)

On this page, you'll see a number of fields, many of which are pre-populated by Odyssey:

#### Info
![Campaign Info](images/campaign_info.png)

- **Account**: Pre-populated from Odyssey, represents the account number of the campaign
- **Name**: Prepopulated from Odyssey, represents the name of the campaign.
- **Campaign Type**: Prepopulated from Odyssey, the type of campaign. Can be one of the following:
  + Country - a country fund
  + General - The Peace Corps Fund _or_ the PCPP General/Global Fund
  + Sector - a sector fund
  + Memorial - a memorial fund
  + Other - an other type, for instance Let Girls Learn
- **Country**: If the campaign is associated with a specific country, click the magnifying glass to select the corresponding country. This is pre-populated for Country funds.
- **Icon**: An icon image that can be used to represent the campaign. For instance, this is typically an image of the Volunteer in Memorial Funds. Should be **120px by 120px**. For instructions on uploading a photo, see the [Uploading Media](media.md#uploading-media).
- **Featured Image**: This is the image that appears at the top of the Campaign's page. If no picture is provided, a default alternate is shown. Uploaded images should be **1100px wide by 454px tall**. For instructions on uploading a photo, see [Uploading Media](media.md#uploading-media).

#### Text
![Campaign Text](images/campaign_text.png)

- **Slug**: Automatically generated from the Title, this will be the URL of the campaign page. It is suggested to not edit this.
- **Description**: The description is automatically imported from Odyssey, and uses a simple editor to provide rich text and imagery. For more on the functionality of the Description field, see [Rich Content Editing](media.md#rich-content-editing).
- **Abstract**: A shorter version of the description, max of 255 characters.
- **Tagline**: A shorter title, specifically used in areas where the full title may not work well.
- **Call**: A Call to action for buttons prompting the user to continue on. For instance, for Let Girls Learn, this is set to "DONATE NOW".
- **Published**: By default this is "off". Checking the published button makes the campaign visible on the website.

Click `Save` and the project will be live on the website, assuming `Published` has been selected.

## Featuring a Campaign

The site offers the ability to feature a campaign, giving it promienence on the homepage.

![Featured Campaign](images/featuredcampaign.png)

To feature a campaign, select Featured Campaign in the admin panel. You'll be presented with the Featured Campaign administrative page:

![Featured Campaign Admin](images/featuredcampaignadmin.png)

**Important**: Only _one_ featured campaign may exist at a time. 

To feature a campaign, or to change the existing featured campaign to a new one, click `Add Featured Campaign +` in the top right of the screen. You'll be presented with two drop down menus:

![Add Featured Campaign](images/addfeaturedcampaign.png)

- **Campaign**: Select the campaign to feature
- **Image**: Select the landing page image to use (or select the green + icon to add a new image). Should be 1100px wide by 589px tall.

Additionally, there are several additional fields that can be specified in the Campaigns' `Campaign` admin panel (see [Creating a New PCPP Campaign](##creatingediting-pcpp-campaigns)). 

- **Call**: A Call to action for buttons prompting the user to continue on. For instance, for Let Girls Learn, this is set to "DONATE NOW".
- **Tagline**: A shorter subtitle. For Let Girls Learn, this is set to "Join the Peace Corps in Supporting Girls' Education Efforts around the World through Let Girls Learn".

## Featuring a Project

The site offers the ability to feature an arbitrary number of PCPP projects. We suggest featuring **no more** than three projects at a time.

![Featured Projects](images/featuredprojects.png)

To change Featured Projects, go to the Featured Projects section of the admin site.

![Featured Projects Admin](images/featuredprojectadmin.png)

Each individual project that is currently featured is listed. To unfeature a project, click the title of the project, then click "DELETE" at the bottom of the page. This will only remove the project's featured status from the site - it will not delete the project entirely.

To feature a new project, click `Add Featured Project +` in the top right. 

![Add Featured Project](images/addfeaturedproject.png)

- **Project**: Use the magnifiying glass icon to open up a menu of all projects, and select the project you wish to feature.
- **Image**: Select the image to use on the homepage (or select the green + icon to add a new image). Should be 525px wide by 320px tall.

Additionally, there are several additional fields that can be specified in the Project's `Project` admin panel (see [Creating/Editing a PCPP Project](#creatingediting-pcpp-projects)). 

- **Tagline**: Used as the title of the project on the homepage.
- **Abstract**: Used as the description of the project on the homepage.