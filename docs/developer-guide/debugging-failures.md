<h1>Debugging Failures/h1>

In this section:

[TOC]

<hr>

When attempting to resolve issues, a number of potential areas should be checked for errors. For most of these errors, the best way to diagnose is to `SSH` in to the affected machine.

## SSHing in to Machines
You'll need to have a copy of the SSH Private Key specified in the CloudFormation deployment script. For servers in private subnets, you'll need to use SSH Agent Forwarding to tunnel through the NAT.

### Machines in Public Subnets
SSHing in to machines in Public Subnets (eg. Admin Server, File Transfer Server) can be accomplished with the following:

```bash
$ ssh -i /path/to/key.pem ubuntu@server-hostname.peacecorps.gov
```

### Machines in Private Subnets
To get in to private subnet machines (Web Application Servers or PayGov Servers), you'll need to use SSH agent forwarding:

```bash
$ ssh -i /path/to/key.pem -A ubuntu@nat-hostname.peacecorps.gov ssh -A ubuntu@server-ip-address
```

**Note**: When debugging errors in machines part of autoscaling groups, such as application servers, you may need to check logs in multiple servers to fully understand the error.

## Application Errors (404's, 500's, non-responsive pages)

After SSHing in to the affected machine(s), check the following logs for errors:

- `/var/log/webapp.log` (Django Application Log)
- `/var/log/gunicorn/*.log`
- `/var/log/nginx/*.log`

## PayGov Errors
First, check [Application Errors](#application-errors) on pay.gov servers. You may also want to check the nginx logs on the NAT machine, as that machine proxies requests for pay.gov.

## Odyssey Errors
If errors are encountered with Odyssey transfers, check the following logs for errors:

- `/var/log/webapp.log`
- `/var/log/syslog` (check for cron job failures)
- `/var/log/auth.log` (check for failed SFTP logins from Peace Corps)