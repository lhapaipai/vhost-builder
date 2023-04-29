from lib.vhost import get_vhost_conf

https = True
domain = 'hello.world-cloud.com'
path = '/home/hugues/projets/hello.world'
php = '8.1'
wildcard_alias = False

vhost_str = get_vhost_conf(https, domain, path, php, wildcard_alias)

print(vhost_str)
