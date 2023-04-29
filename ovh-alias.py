#!/usr/bin/python

from argparse import ArgumentParser
import json
import ovh
import os
import sys

if os.geteuid() == 0:
    print('You don''t need root privileges to run this script')

parser = ArgumentParser(description="Add/Remove new CNAME to ovh")
parser.add_argument(
    'action',
    choices=['add', 'remove'],
    help="action to do"
)
parser.add_argument(
    "alias_domain", help="your new alias domain name ex: <your-subdomain>.<domain>.com")
parser.add_argument(
    "canonical_domain", help="your canonical domain name ex: vps.server.<domain>.com")

args = parser.parse_args()

action = args.action
domain = args.alias_domain

domain_splitted = domain.split('.')
principal_domain = '.'.join(domain_splitted[-2:])
sub_domain = '.'.join(domain_splitted[:-2])

canonical_domain = args.canonical_domain
if canonical_domain[-1] != '.':
    canonical_domain += '.'

ovh_conf_file = '/etc/ovh/.ovh.ini'
client = ovh.Client(config_file=ovh_conf_file)

# print("welcome", client.get('/me')['firstname'])

records = client.get(F'/domain/zone/{principal_domain}/record',
                     fieldType='CNAME',
                     subDomain=sub_domain
                     )

if len(records) > 0:
    record_id = records[0]
else:
    record_id = None

is_modified = False

if action == 'add':
    if record_id:
        print('already exist')
    else:
        record_infos = client.post(
            F'/domain/zone/{principal_domain}/record',
            fieldType='CNAME',
            subDomain=sub_domain,
            target=canonical_domain,
            ttl=0
        )
        print(json.dumps(record_infos, indent=4))
        is_modified = True
else:
    if record_id == None:
        print('already deleted')
    else:
        client.delete(F'/domain/zone/{principal_domain}/record/{record_id}')
        print('record deleted')
        is_modified = True

if is_modified:
    print('ovh refresh')
    client.post(F'/domain/zone/{principal_domain}/refresh')
