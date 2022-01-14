#!/usr/bin/python

from argparse import ArgumentParser
from config import apache_root, email, apache_log, uid, gid, apache_certs
from pathlib import Path

import subprocess
import re
import os
import sys
import inquirer

if os.geteuid() != 0:
    print('You need root privileges to run this script')
    sys.exit(1)

parser = ArgumentParser(description="Create a virtual host")
parser.add_argument("domain", help="your domain name for your virtual host")
parser.add_argument(
    "--conf-dir",
    help="specify your local directory where you want to place your vhost conf file"
)
args = parser.parse_args()

domain = args.domain
custom_conf_dir = args.conf_dir
cwd = Path(os.getcwd())

error_log_file = F'ErrorLog {apache_log}/{domain}-error.log'
access_log_file = F'CustomLog {apache_log}/{domain}-access.log vcombined'

sites_available_dir = apache_root / 'sites-available'

sites_enabled_path = apache_root / 'sites-enabled' / F'{domain}.conf'
sites_available_path = sites_available_dir / F'{domain}.conf'

if custom_conf_dir:
    conf_dir_path = cwd / custom_conf_dir
    conf_dir_path = conf_dir_path.resolve()

    certs_dir_path = conf_dir_path

    if not conf_dir_path.exists():
        conf_dir_path.mkdir(parents=True)
        os.chown(conf_dir_path, uid, gid)
else:
    conf_dir_path = sites_available_dir
    certs_dir_path = apache_certs

conf_file_path = conf_dir_path / F'{domain}.conf'

if conf_file_path.exists():
    print('A conf file already exist for this domain')
    sys.exit(2)


questions = [
    inquirer.List(
        'php_version',
        message="What's your PHP version ?",
        choices=['8.0', '7.4', '7.3']
    ),
    inquirer.List(
        'https',
        message="Do you want https ?",
        choices=["No", "Yes, with mkcert", "Yes, with let's encrypt"]
    )
]

result = inquirer.prompt(questions)

if result['php_version'] == '8.0':
    php_handler = 'proxy:unix:/run/php-fpm/php-fpm.sock|fcgi://localhost/'
elif result['php_version'] == '7.4':
    php_handler = 'proxy:unix:/run/php-fpm7/php-fpm.sock|fcgi://localhost/'
elif result['php_version'] == '7.3':
    php_handler = 'proxy:unix:/run/php73-fpm/php-fpm.sock|fcgi://localhost/'
else:
    print('Unknown PHP Version')
    sys.exit(3)


# /etc/hosts
with Path('/etc/hosts').open('r') as fdin:
    hosts_lines = fdin.readlines()

is_present_in_hosts = False
domain_escaped = re.escape(domain)
regex = F'127\.0\.0\.1\s+({domain_escaped})$'

for line in hosts_lines:
    if line[0] == '#':
        continue

    match = re.search(regex, line)
    if match and match.group(1) == domain:
        is_present_in_hosts = True

if not is_present_in_hosts:
    with Path('/etc/hosts').open('a') as fdout:
        fdout.write(F'127.0.0.1  {domain}\n')

    print(F"add {domain} into /etc/hosts")


# Apache
if result['https'] == "Yes, with mkcert":

    public_key_path = certs_dir_path / F'{domain}.pem'
    private_key_path = certs_dir_path / F'{domain}.key.pem'
    # subprocess.run([
    #     'sudo', '-u', 'lhapaipai',
    #     'bash', '-c'
    #     F'mkcert -cert-file {public_key_path} -key-file {private_key_path} {domain}'
    # ])
    # if custom_conf_dir:
    #     os.chown(public_key_path, uid, gid)
    #     os.chown(private_key_path, uid, gid)

    print('run :')
    print(
        F'mkcert -cert-file {public_key_path} -key-file {private_key_path} {domain}')

    virtual_host_str = F"""
<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain}
    Redirect "/" "https://{domain}/"
</VirtualHost>
<VirtualHost *:443>
    ServerAdmin {email}
    ServerName {domain}
    DocumentRoot '{cwd}'
    <Directory '{cwd}'>
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    <FilesMatch \.php$>
        SetHandler '{php_handler}'
    </FilesMatch>

    {error_log_file}
    {access_log_file}

    SSLEngine on
    SSLCertificateFile {public_key_path}
    SSLCertificateKeyFile {private_key_path}
</VirtualHost>
"""
elif result['https'] == "Yes, with let's encrypt":

    virtual_host_str = F"""
<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain}
    # Redirect "/" "https://{domain}/"

    <Directory '{cwd}'>
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    <FilesMatch \.php$>
        SetHandler '{php_handler}'
    </FilesMatch>

    {error_log_file}
    {access_log_file}
</VirtualHost>
<VirtualHost *:443>
    ServerAdmin {email}
    ServerName {domain}
    DocumentRoot '{cwd}'
    <Directory '{cwd}'>
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    <FilesMatch \.php$>
        SetHandler '{php_handler}'
    </FilesMatch>

    {error_log_file}
    {access_log_file}

    #SSLEngine on
    #SSLCertificateFile /etc/letsencrypt/live/{domain}/fullchain.pem
    #SSLCertificateKeyFile /etc/letsencrypt/live/{domain}/privkey.pem
    #Include /etc/letsencrypt/options-ssl-apache.conf

</VirtualHost>
"""
    print("run : sudo certbot --apache certonly")
    print("and decomment conf file")
else:
    virtual_host_str = F"""
<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain}
    DocumentRoot '{cwd}'
    <Directory '{cwd}'>
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    <FilesMatch \.php$>
        SetHandler '{php_handler}'
    </FilesMatch>

    {error_log_file}
    {access_log_file}
</VirtualHost>
"""


with conf_file_path.open('w') as fw:
    fw.write(virtual_host_str)

sites_enabled_path.symlink_to(sites_available_path)

if custom_conf_dir:
    os.chown(conf_file_path, uid, gid)
    sites_available_path.symlink_to(conf_file_path)

if result['https'] != "Yes, with mkcert":
    subprocess.run(['apachectl', 'graceful'])

print(F'Nouveau site sur http://{domain}')
