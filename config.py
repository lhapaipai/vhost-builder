from configparser import ConfigParser
from pathlib import Path
from pwd import getpwnam
import os

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

config = ConfigParser()
config.read(dir_path / 'configuration.ini')

apache_certs = Path(config['global']['apache_certs'])
apache_root = Path(config['global']['apache_root'])
apache_log = Path(config['global']['apache_log'])
email = config['global']['email']

uid = getpwnam(config['global']['local_user']).pw_uid
gid = getpwnam(config['global']['local_user']).pw_gid
