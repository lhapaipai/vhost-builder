#!/usr/bin/python

from argparse import ArgumentParser
from lib.config import sites_available_dir, sites_enabled_dir
from lib.vhost import is_vhost_https

import os
import sys
import subprocess

parser = ArgumentParser(description="Enable a virtual host")
parser.add_argument("domain", help="your domain name for your virtual host")

args = parser.parse_args()

domain = args.domain
cwd = os.getcwd()

conf_file = sites_available_dir / F'{domain}.conf'
symlink = sites_enabled_dir / F'{domain}.conf'

if os.geteuid() != 0:
    print('You need root privileges to run this script')
    sys.exit(1)

if not conf_file.exists():
    print('No configured site for this domain.')
    sys.exit(2)

if symlink.is_symlink():
    symlink.unlink()

subprocess.run(['apachectl', 'graceful'])

https = is_vhost_https(conf_file)
print(F'Site disabled sur http{"s" if https else ""}://{domain}')
