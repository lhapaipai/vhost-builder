#!/usr/bin/python

from argparse import ArgumentParser
from pathlib import Path
from lib.config import sockets_by_php_version, sites_available_dir, sites_enabled_dir, write_host, certs_engine, certs_dir, email, certs_user
from lib.vhost import get_vhost_conf
from lib.hosts import add_to_hosts

import subprocess
import os
import sys
import inquirer

if os.geteuid() != 0:
    print('You need root privileges to run this script')
    sys.exit(1)

cwd = os.getcwd()

parser = ArgumentParser(description="Create a virtual host")
parser.add_argument(
    "domain", help="your domain name for your virtual host")
parser.add_argument(
    "path", type=Path, help="the path to your documentRoot", nargs='?', default=cwd)
parser.add_argument('--php', default=None)
parser.add_argument('--https', default=None, action='store_true')
parser.add_argument('--http', default=None, action='store_true')
parser.add_argument('--non-interactive', default=False, action='store_true')
parser.add_argument('--wildcard-alias', default=False, action='store_true')

args = parser.parse_args()

domain = args.domain
path = args.path
wildcard_alias = args.wildcard_alias

if args.php == None:
    if args.non_interactive:
        raise Exception('you must provide php version')

    result = inquirer.prompt([inquirer.List(
        'php',
        message="What's your PHP version ?",
        choices=sockets_by_php_version
    )])
    php = result['php']
else:
    if not sockets_by_php_version.get(args.php):
        raise Exception('you must provide valid php version')
    php = args.php

if args.https == None and args.http == None:
    if args.non_interactive:
        raise Exception('you must provide http or https')

    result = inquirer.prompt([inquirer.List(
        'secure',
        message="Do you want https ?",
        choices=['Yes', 'No']
    )])
    https = True if result['secure'] == 'Yes' else False
else:
    https = True if args.https else False

if wildcard_alias and https and certs_engine != 'certbot_ovh':
    print('in https wildcard_alias only compatible with certbot_ovh')
    sys.exit(1)

# print('domain', domain)
# print('path', path)
# print('php ', php)
# print('https ', https)
# print('wildcard_alias ', wildcard_alias)


conf_path = sites_available_dir / F'{domain}.conf'

if conf_path.exists():
    print('A conf file already exist for this domain')
    sys.exit(2)

if write_host:
    add_to_hosts(domain)

http_vhost_str = get_vhost_conf(False, domain, path, php, wildcard_alias)
https_vhost_str = get_vhost_conf(True, domain, path, php, wildcard_alias)

# create conf file
with conf_path.open('w') as fw:
    fw.write(http_vhost_str)

# enable vhost
(sites_enabled_dir / F'{domain}.conf').symlink_to(conf_path)

subprocess.run(['apachectl', 'graceful'])

if https:
    try:
        if certs_engine == 'mkcert':
            subprocess.run([
                'sudo', '-u', certs_user, '--', 'bash', '-c',
                F'mkdir {certs_dir}/{domain} && mkcert -cert-file {certs_dir}/{domain}/fullchain.pem -key-file {certs_dir}/{domain}/privkey.pem {domain}'
            ])

        if certs_engine == 'certbot_apache':
            subprocess.run(['certbot', 'certonly', '--apache', '-d', domain])

        if certs_engine == 'certbot_ovh':
            ovh_conf_file = '/etc/ovh/.ovhapi'

            if wildcard_alias:

                subprocess.run([
                    'certbot', 'certonly', '--non-interactive',
                    '--dns-ovh', '--dns-ovh-credentials', ovh_conf_file,
                    '--agree-tos', '--email', email,
                    '-d', domain,
                    '-d', '*.'+domain
                ])

            else:
                subprocess.run([
                    'certbot', 'certonly', '--non-interactive',
                    '--dns-ovh', '--dns-ovh-credentials', ovh_conf_file,
                    '--agree-tos', '--email', email,
                    '-d', domain
                ])

        with conf_path.open('w') as fw:
            fw.write(https_vhost_str)

        subprocess.run(['apachectl', 'graceful'])

    except:
        print("ssl certificate generation error your site is http only")
        https = False

print(F'New site on http{"s" if https else ""}://{domain}')
