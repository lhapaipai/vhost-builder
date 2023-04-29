from pathlib import Path
import re


def add_to_hosts(domain):

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

        print(F"added {domain} into /etc/hosts")


def remove_from_hosts(domain):
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
