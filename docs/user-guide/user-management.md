<h1>User Management</h1>
In this section:

[TOC]

<hr>

The Authentication and Authorization section of the CMS is used to manage **users** and **groups**. Users are internal individuals who have the ability to manage various aspects of the site.

## Groups
Groups are currently unused, but could be expanded in the future to offer various levels of control to types of users (eg. editors, administrators, etc).

## Users
The **users** section is used to manage each individual member who has access to the CMS. A few general guidelines for users that are important to remember:

- In the current iteration of the site, each user has full administrative access. That means they can create new users, manage all aspects of the site, and take potentially disastrous actions. It's important that new users are created with care, and that these users understand how to use the site.
- User accounts are designed to be for _individuals_. **Important**: You should not create a generic user account for multiple users (eg. an "intern" user account or a user account for a specific work group).

### Adding A User
To create a new user, click "Add User +" in the upper right hand corner of the Users screen:

![Add User Button](images/add_user.png)

Enter the following information:

- **Username**: The user's email address
- **Password**: The initial password for the user (must follow the standard [Password Requirements](https://github.com/Threespot/peacecorps-site/wiki/Getting-Started#password-requirements))
- **Password confirmation**: The same password as above, for verification

If you need help generating a password, we recommend using https://lastpass.com/generatepassword.php to make one.

**Important Note**: You should never send a user their password via email. Instead, we recommend using a service like Fugacious to generate a temporary "secret message" that can contain the password, and emailing them a link to the message.

Click **Save**, and you'll be brought to a screen asking for additional information.

- **First Name**: Enter the user's first name
- **Last Name**: Enter the user's last name
- **Email address**: Enter the user's email address
- Ensure **Staff Status** is checked
- Ensure **Superuser status** is checked
- Click **Save** to complete the process

### Changing a user's password
To change a user password, click on their email address from the Users page to get to the "Change User" page. From there, you'll see a link to change their password ("Raw passwords are not stored, so there is no way to see this user's password, but you can change the password **using this form**.")

![Change Password text](images/change_password.png)

The new password for the user must follow the standard [Password Requirements](https://github.com/Threespot/peacecorps-site/wiki/Getting-Started#password-requirements). If you need help generating a password, we recommend using https://lastpass.com/generatepassword.php to make one.

**Important Note**: You should never send a user their password via email. Instead, we recommend using a service like Fugacious to generate a temporary "secret message" that can contain the password, and emailing them a link to the message.

### Deleting a User
To delete a user, click on their email address from the Users page to get to the "Change User" page. From there, scroll to the bottom of the page, where you'll see a "Delete" link.
![Delete User](images/delete_user.png)