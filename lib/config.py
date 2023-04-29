from configparser import ConfigParser
from pathlib import Path
from pwd import getpwnam
import os

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

config = ConfigParser()
config.read(dir_path / '../configuration.ini')

apache_root = Path(config['global']['apache_root'])
sites_available_dir = apache_root / 'sites-available'
sites_enabled_dir = apache_root / 'sites-enabled'


apache_log = Path(config['global']['apache_log'])
email = config['global']['email']

certs_dir = Path(config['global']['certs_dir'])
certs_engine = config['global']['certs_engine']
certs_user = config['global']['certs_user']

write_host = config.getboolean('global', 'write_host')

sockets = [
    socket.split('|') for socket in config['global']['sockets'].split(',')
]
sockets_by_php_version = {
    php_version: socket for (php_version, socket) in sockets
}
