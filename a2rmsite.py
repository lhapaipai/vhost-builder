#!/usr/bin/python

from argparse import ArgumentParser
from pathlib import Path
from lib.config import sockets_by_php_version, sites_available_dir, sites_enabled_dir, certs_engine, certs_dir, write_host
from lib.hosts import remove_from_hosts
from lib.vhost import is_vhost_https

import subprocess
import re
import os
import sys
import inquirer
import shutil

if os.geteuid() != 0:
    print('You need root privileges to run this script')
    sys.exit(1)

parser = ArgumentParser(description="Remove a virtual host")
parser.add_argument("domain", help="your domain name for your virtual host")

args = parser.parse_args()

domain = args.domain

# remove symlink if vhost is enabled
conf_file_link = sites_enabled_dir / F'{domain}.conf'
if conf_file_link.is_symlink():
    conf_file_link.unlink()

# remove conf file
conf_file_path = sites_available_dir / F'{domain}.conf'
has_https = is_vhost_https(conf_file_path)

if conf_file_path.exists():
    conf_file_path.unlink()

if has_https:
    # revoke and delete certs files
    if certs_engine == 'mkcert':
        if (certs_dir / domain).exists():
            shutil.rmtree(certs_dir / domain)
    else:
        try:
            subprocess.run([
                'certbot', 'revoke', '--cert-name', domain, '--delete-after-revoke'
            ])
        except:
            print('certbot certificate revocation error your site is removed but your certificate is always present')

if write_host:
    remove_from_hosts(domain)

subprocess.run(['apachectl', 'graceful'])
