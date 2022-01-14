#!/usr/bin/python

from argparse import ArgumentParser
from config import apache_root, email, apache_log, apache_certs
from pathlib import Path
import re
import os
import sys
import inquirer
import subprocess

parser = ArgumentParser(description="Create a virtual host")
parser.add_argument("domain", help="your domain name for your virtual host")

args = parser.parse_args()

domain = args.domain
cwd = os.getcwd()

if os.geteuid() != 0:
    print('You need root privileges to run this script')
    sys.exit(1)

sites_enabled_dir = apache_root / 'sites-enabled'
sites_available_dir = apache_root / 'sites-available'


sites_enabled_path = sites_enabled_dir / F'{domain}.conf'
sites_available_path = sites_available_dir / F'{domain}.conf'

if sites_available_path.is_symlink():

    conf_file_path = sites_available_path.readlink()
    certs_dir_path = conf_file_path.parent
else:
    conf_file_path = sites_available_path
    certs_dir_path = apache_certs


if not conf_file_path.exists():
    print('No configured site for this domain.')
    sys.exit(2)

# delete conf files
conf_file_path.unlink()
if sites_enabled_path.is_symlink():
    sites_enabled_path.unlink()

if sites_available_path.is_symlink():
    sites_available_path.unlink()

# delete certs files
public_key_path = certs_dir_path / F'{domain}.pem'
private_key_path = certs_dir_path / F'{domain}.key.pem'

if public_key_path.exists():
    public_key_path.unlink()

if private_key_path.exists():
    private_key_path.unlink()

# delete /etc/hosts line
with Path('/etc/hosts').open('r') as fdin:
    hosts_lines = fdin.readlines()

domain_escaped = re.escape(domain)
regex = F'127\.0\.0\.1\s+({domain_escaped})$'

with Path('/etc/hosts').open('w') as fdout:
    for line in hosts_lines:

        match = re.search(regex, line)
        if match and match.group(1) == domain:
            print(F'remove {domain} from /etc/hosts')
        else:
            fdout.write(line)

subprocess.run(['apachectl', 'graceful'])
