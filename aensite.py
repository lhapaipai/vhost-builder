#!/usr/bin/python

from argparse import ArgumentParser
from config import apache_root, email, apache_log
import os
import sys
import inquirer
import subprocess

parser = ArgumentParser(description="Enable a virtual host")
parser.add_argument("domain", help="your domain name for your virtual host")

args = parser.parse_args()

domain = args.domain
cwd = os.getcwd()

conf_file = apache_root / 'sites-available' / F'{domain}.conf'
symlink = apache_root / 'sites-enabled' / F'{domain}.conf'

if os.geteuid() != 0:
    print('You need root privileges to run this script')
    sys.exit(1)

if not conf_file.exists():
    print('No configured site for this domain.')
    sys.exit(2)

if not symlink.is_symlink():
    symlink.symlink_to(conf_file)

subprocess.run(['apachectl', 'graceful'])


print(F'Site activé sur http://{domain}')
