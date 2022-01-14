from argparse import ArgumentParser
from config import apache_root, email, apache_log
import os
import sys
import inquirer
import re
from pathlib import Path
parser = ArgumentParser(description="Create a virtual host")
parser.add_argument("domain", help="your domain name for your virtual host")

args = parser.parse_args()

domain = args.domain
cwd = os.getcwd()

error_log_file = F'ErrorLog {apache_log}/{domain}-error.log'
access_log_file = F'CustomLog {apache_log}/{domain}-access.log vcombined'

conf_file = apache_root / 'sites-available' / F'{domain}.conf'
symlink = apache_root / 'sites-enabled' / F'{domain}.conf'

# print(domain, cwd, apache_root)


# if os.geteuid() != 0:
#     print('You need root privileges to run this script')
#     sys.exit(1)

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


# with Path('/etc/hosts').open('w') as fdout:
#     for line in hosts_lines:

#         match = re.search(regex, line)
#         if match and match.group(1) == domain:
#             print(F'remove {domain} from /etc/hosts')
#         else:
#             fdout.write(line)
