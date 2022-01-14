
install:

	sudo cp -r . /opt/vhost-builder

	sudo ln -f -s /opt/vhost-builder/amksite.py /usr/local/bin/amksite
	sudo ln -f -s /opt/vhost-builder/armsite.py /usr/local/bin/armsite
	sudo ln -f -s /opt/vhost-builder/aensite.py /usr/local/bin/aensite
	sudo ln -f -s /opt/vhost-builder/adissite.py /usr/local/bin/adissite
	sudo ln -f -s /opt/vhost-builder/alssites.py /usr/local/bin/alssites

	sudo cp share/apache.bash_completion /usr/share/bash-completion/completions/vhost-builder
	sudo cp share/apache.bash_completion /etc/bash_completion.d/vhost-builder

uninstall:

	sudo rm -rf /opt/vhost-builder

	sudo rm -rf /usr/local/bin/amksite
	sudo rm -rf /usr/local/bin/armsite
	sudo rm -rf /usr/local/bin/aensite
	sudo rm -rf /usr/local/bin/adissite
	sudo rm -rf /usr/local/bin/alssites

	sudo rm -rf /usr/share/bash-completion/completions/vhost-builder
	sudo rm -rf /etc/bash_completion.d/vhost-builder