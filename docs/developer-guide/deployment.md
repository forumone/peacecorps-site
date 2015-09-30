<h1>Deployment</h1>

In this section:

[TOC]

<hr>

The platform is currently deployed in Amazon Web Services in two identical environments - `staging` and `production`. Each environment exists within its own Virtual Private Cloud and has robust autoscaling and performance management built in.

![Infrastructure](images/infrastructure.png)

This guide is designed to get you up and running with deploying the Peace Corps site on Amazon Web Services in a scalable, distributed architecture.

For more information and resources, see the complete [code base](https://github.com/Threespot/peace-corps-infrastructure) for deployments and infrastructure.

## Architecture
The infrastructure of donate.peacecorps.gov is split in to some basic units, noted below. Each of these is provisioned automatically by CloudFormation.

### VPC
We use an Amazon Virtual Private Cloud to first create an isolated unit in AWS. Within this VPC, we have four _subnets_ - two Public subnets (for public resources, in different availibility zones) and two Private Subnets (for private resources, in different availibility zones).

### Security Groups
We further have a number of _Security Groups_ designed to block or allow traffic from various sources, incluging public traffic, traffic from pay.gov, internal VPC traffic, or traffic from Peace Corps Headquarters.

### RDS
We use AWS' Relational Database Service to provide a PostgreSQL database to the application.

### S3
We use S3 to both store instance sensitive data (encrypted, of course) and have static and media assets available to Django. EC2 IAM Roles are used to selectively provide access to S3 resources.

### Instance Types
We have a few instance types that we use:

#### NAT
The NAT machine sits in a public subnet with an Elastic IP address on it. This allows us to offer a static IP address to pay.gov and route public traffic out of the VPC. The NAT has `nginx` installed to proxy traffic to the `paygov` Elastic Load Balancers in order to give us a static IP. It only accepts traffic from known pay.gov IP addresses.

#### Webservers
Webservers (provisioned via `WebASGroup`, `WebLaunchConfig`, and `WebELB`) are located in an AWS Autoscaling Group. They serve the bulk of traffic to public users. The Webservers sit in a private subnet and are load balanced by an ELB sitting in the public subnet.

#### Paygov
Paygov servers (provisioned via `PayGovASGroup`, `PayGovLaunchConfig`, and `PayGovELB`) provide protected access to pay.gov for transaction information. As part of this, the NAT instance provides a static IP proxy that goes to the PayGovELB. They otherwise are functionally identical to Webservers.

### Admin
The Admin server (provisioned via `AdminASGroup` and `AdminLaunchConfig`) provides for Django admin panel access, database migration and static collection, and holds an SFTP server for Peace Corps to upload bulk transaction data in to the system.

---

## Before You Begin
You'll need a few things before you begin, both locally and in your Amazon Web Services account:

### Locally
- [Packer](https://www.packer.io) installed
- A `packer_vars.json` file created in the `packer/` directory with the following format:

```json
{
    "aws_access_key": "YOURAWSACCESSKEY",
    "aws_secret_key": "YOURAWSSECRETKEY",
    "vpc_id": "VPCID",
    "subnet_id": "PUBLICSUBNETID"
}
```

_Note that `vpc_id` and `subnet_id` should be a VPC and Public Subnet you create in AWS just for Packer. Don't use the VPC for the production application here._

### Online
You'll need to do a little bit of groundwork online as well:

1. Create a Route53 Hosted Zone for the domain name you want to use.

For this project, we deletegate the `NS` records for `donate.peacecorps.gov` to Route53. Keep the Hosted Zone ID Route 53 provides you handy as you'll need it later.

2. A Deploy Token from GitHub
You'll need a GitHub deploy token to grab updates from Git.

3. Domain Names
You'll need to know a few domain names you will want to use. In particular:

- **DomainName**: the main domain for the application (eg. `donate.peacecorps.gov`). You'll need to manually create this in Route 53 and point an `ALIAS` to the `WebELB` after the stack is created.
- **PayGovDomainName**: the endpoint URL for pay.gov. You'll need to manually create this in Route 53 and point an `A` to the `NAT` Elastic IP address after the stack is created.
- **AdminDomainName**: the URL for the admin panel. This will be automatically created by the stack.
- **FileTransferDomainName**: the URL for the SFTP server. This will be automatically created by the stack.

5. Elastic IP address
You'll need to create an Elastic IP address for the application to use and note the `AllocationID`, which you'll need later.

6. S3 Buckets
You'll need a few S3 buckers:

- Media Bucket
_Just create this, you'll provide the name to CloudFormation_

- Static Bucket
_Just create this, you'll provide the name to CloudFormation_

- Secrets Bucket
_We use peacecorps-secrets_. Inside this bucket, you'll need the following organizational structure.

```
peacecorps-secrets
|
|- staging/ (if used)
|  - web/
|    - all/
|      - pubring.gpg.enc
|      - trustdb.gpg.enc
|    - admin/
|      - {{AdminDomainName}}.chained.crt.enc
|      - {{AdminDomainName}}.key.enc
|    - paygov/
|      - {{PayGovDomainName}}.chained.crt.enc
|      - {{PayGovDomainName}}.key.enc
|      - secring.gpg.enc
|    - web/
|      - {{DomainName}}.chained.crt.enc
|      - {{DomainName}}.key.enc
|- production/ (if used)
|  - web/
|    - all/
|      - pubring.gpg.enc
|      - trustdb.gpg.enc
|    - admin/
|      - {{AdminDomainName}}.chained.crt.enc
|      - {{AdminDomainName}}.key.enc
|    - paygov/
|      - {{PayGovDomainName}}.chained.crt.enc
|      - {{PayGovDomainName}}.key.enc
|      - secring.gpg.enc
|    - web/
|      - {{DomainName}}.chained.crt.enc
|      - {{DomainName}}.key.enc
```

Replace {{DomainName}} with the DomainName mentioned above, etc. In this structure, *.chained.crt.enc is a SSL chained certificate and *.key.enc is a SSL certificate. Everything should be encrypted before you upload. You can accomplish this with the following command:

```bash
openssl aes-256-cbc -a -salt -in filename.ext -out filename.ext.enc
```

It will prompt you for a passphrase, make sure to use the same passphrase for each file and note it as you'll need to provide it later on.


## Running Packer
You'll need to generate two AMIs. You can do this with the following command prompts, run from inside the `packer/` directory:

```bash
packer build -var-file=packer_vars.json web.json
```

```bash
packer build -var-file=packer_vars.json nat.json
```

Make sure you note the AMI IDs generated from each as you'll need them later.

## Uploading to CloudFormation

1. Go to CloudFormation (https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filter=active) in your AWS Console.

2. Select Create Stack

3. Enter a name for the stack, and upload the `cloudformation.json` template

4. Provide the data requested. I've highlighted some fields to pay attention to:

**AdminDomainName**
The admin domain name you created above

**Client ID**
For Threespot purposes, the client ID. Peace Corps is `PC-20140812-20190811-01`.

**DBPassword**
Enter a password for RDS.

**DecryptionKey**
The key you used in `openssl` for the secrets uploaded to S3.

**AdminDomainName**
The domain name you created above

**ReleaseTag**
The release tag from https://github.com/Threespot/peacecorps-site/releases to deploy.

Hit deploy and you should be good to go after 10-20 minutes!