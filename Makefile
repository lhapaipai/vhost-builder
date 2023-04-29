
install:
	cp -r . /opt/vhost-builder

	ln -f -s /opt/vhost-builder/a2mksite.py /usr/local/bin/a2mksite
	ln -f -s /opt/vhost-builder/a2rmsite.py /usr/local/bin/a2rmsite
	ln -f -s /opt/vhost-builder/a2lssites.py /usr/local/bin/a2lssites
	ln -f -s /opt/vhost-builder/ovh-alias.py /usr/local/bin/ovh-alias

	cp share/apache.bash_completion /usr/share/bash-completion/completions/vhost-builder
	cp share/apache.bash_completion /etc/bash_completion.d/vhost-builder

install-arch:
	ln -f -s /opt/vhost-builder/a2ensite.py /usr/local/bin/a2ensite
	ln -f -s /opt/vhost-builder/a2dissite.py /usr/local/bin/a2dissite

install-credentials:
	mkdir /etc/ovh
	cp ./.ovh.ini /etc/ovh/.ovh.ini
	cp ./.ovhapi /etc/ovh/.ovhapi
	chown -R root:root /etc/ovh
	chmod 644 /etc/ovh/.ovh.ini
	chmod 600 /etc/ovh/.ovhapi

uninstall:
	rm -rf /opt/vhost-builder
	rm -rf /usr/local/bin/{a2mksite,a2rmsite,a2lssites,ovh-alias}
	rm -rf /usr/share/bash-completion/completions/vhost-builder
	rm -rf /etc/bash_completion.d/vhost-builder

uninstall-credentials:
	rm -rf /etc/ovh
