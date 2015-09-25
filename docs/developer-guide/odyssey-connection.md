<h1>Odyssey Connection</h1>

In this section:

[TOC]

<hr>

The site connects to Peace Corps Odyssey through a SFTP (FTP over SSH) connection to provide accounting updates of PCPP projects and funds.

## Connection Steps
Inside the VPC, a server (`filetransfer.donate.peacecorps.gov`) exists, which provides a jailed SFTP environment and contains a public key from Peace Corps for authentication.

1. Peace Corps generates an export file and logs in to the SFTP server using their private key, then places the file with a timestamped filename in the `incoming` directory.
2. Every 17 minutes past the hour, a [cron job](https://github.com/18F/peace-corps-infrastructure/blob/master/packer/files/filetransfer/sync_accounting) runs that searches for the latest uploaded file and runs the `sync_accounting` management script in Django to update the database with the files.
3. Every 13 minutes past the hour, a [cron job](https://github.com/18F/peace-corps-infrastructure/blob/master/packer/files/filetransfer/check_incoming_status.sh) runs to see if no files have been uploaded in 24 hours, and sends a warning email if true.
4. Every 27 minutes past the hour, a [cron job](https://github.com/18F/peace-corps-infrastructure/blob/master/packer/files/filetransfer/delete_old_file_transfers) runs and deletes any file transfers older than 7 days.