from lib.config import apache_root, email, apache_log, sockets_by_php_version, certs_dir, certs_engine
import re


def is_vhost_https(conf_file_path):
    has_https = False
    if conf_file_path.exists():
        with(conf_file_path).open('r') as f:
            if 'SSLEngine' in f.read():
                has_https = True
    return has_https


def get_vhost_conf(https, domain, path, php, wildcard_alias=False):
    if not sockets_by_php_version.get(php):
        raise Exception(F'PHP version unknow {php}')

    socket = sockets_by_php_version.get(php)
    error_log_file = F'ErrorLog {apache_log}/{domain}-error.log'
    access_log_file = F'CustomLog {apache_log}/{domain}-access.log combined'

    if wildcard_alias:
        server_alias = F'ServerAlias *.{domain}'

        # domain            hello-world.localhost
        # domain_escaped    hello\\-world\\.localhost
        domain_escaped = re.escape(domain)
        http_to_https_redirect = F"""
    RewriteEngine On
    RewriteCond %{{HTTPS}} off
    RewriteCond %{{HTTP_HOST}} ^{domain_escaped} [NC]
    RewriteRule ^/?(.*)$ https://{domain_escaped}/$1 [L,R=301]

    RewriteCond %{{HTTPS}} off
    RewriteCond %{{HTTP_HOST}} ^(.*)\.{domain_escaped} [NC]
    RewriteRule ^/?(.*)$ https://%1.{domain_escaped}/$1 [L,R=301]
"""
    else:
        server_alias = ''
        http_to_https_redirect = F'Redirect "/" "https://{domain}/"'

    if https:

        if certs_engine == 'certbot_apache' or certs_engine == 'certbot_ovh':
            certInclude = """<IfFile "/etc/letsencrypt/options-ssl-apache.conf">
        Include /etc/letsencrypt/options-ssl-apache.conf
    </IfFile>"""
        else:
            certInclude = ''

        virtual_host_str = F"""
<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain}
    {server_alias}
    {http_to_https_redirect}
</VirtualHost>

<VirtualHost *:443>
    ServerAdmin {email}
    ServerName {domain}
    {server_alias}
    DocumentRoot '{path}'
    <Directory '{path}'>
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    <FilesMatch \.php$>
        SetHandler 'proxy:unix:{sockets_by_php_version.get(php)}|fcgi://localhost'
    </FilesMatch>

    {error_log_file}
    {access_log_file}

    <IfFile "{certs_dir}/{domain}/fullchain.pem">
        SSLEngine on
        SSLCertificateFile {certs_dir}/{domain}/fullchain.pem
        SSLCertificateKeyFile {certs_dir}/{domain}/privkey.pem
    </IfFile>
    {certInclude}
</VirtualHost>
"""
        # print(F"run : sudo certbot certonly --apache -d {domain}")

    else:
        virtual_host_str = F"""
<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain}
    {server_alias}
    DocumentRoot '{path}'
    <Directory '{path}'>
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    <FilesMatch \.php$>
        SetHandler 'proxy:unix:{sockets_by_php_version.get(php)}|fcgi://localhost'
    </FilesMatch>

    {error_log_file}
    {access_log_file}
</VirtualHost>
"""

    return virtual_host_str
