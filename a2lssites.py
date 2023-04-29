#!/usr/bin/python

from argparse import ArgumentParser
from lib.config import apache_root
from pathlib import Path

import subprocess
import re
import os
import sys
import inquirer


sites_available_dir = apache_root / 'sites-available'
sites_enabled_dir = apache_root / 'sites-enabled'

sites_enabled = [file.stem for file in sites_enabled_dir.iterdir()]

for sites_available_file in sites_available_dir.iterdir():
    if sites_available_file.suffix != '.conf':
        continue

    if sites_available_file.stem in sites_enabled:
        enabled = "\033[32m●\033[0m"
    else:
        enabled = "\033[31m●\033[0m"

    with sites_available_file.open('r') as fdin:
        lines = fdin.readlines()

    protocol = server_name = document_root = None

    for line in lines:

        match = re.search('VirtualHost \*:([0-9]+)', line)
        if match:
            protocol = "http://" if match.group(1) == '80' else "https://"

        match = re.search('ServerName\s+([-\w\.]+)\s*$', line)
        if match:
            server_name = match.group(1)

        match = re.search('DocumentRoot\s+[\'\"]([-\.\w\/]+)[\'\"]\s*$', line)
        if match:
            document_root = match.group(1)

        if protocol != None and server_name != None and document_root != None:
            url = "{}{}".format(protocol, server_name)

            print("{} {:<50} {}".format(
                enabled, url, document_root
            ))

            https = server_name = document_root = None


# print(sites_enabled_files)
