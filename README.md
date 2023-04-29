# vhost-builder

Configure automatiquement vos hôtes virtuels apache.
Optimisé pour une utilisation en environnement Linux.
Auto-complétion des noms de domaine avec Bash.

## Installation

les commandes python étant exécutées en tant que root il nous faut :

```console
# installer globalement le package Python inquirer
sudo -H pip install inquirer ovh

# éditer le fichier de configuration
cp configuration.dist.ini configuration.ini

# lancer la copie des fichiers
sudo make install
```

### Https local

`a2mksite` utilise `mkcert` pour générer des certificats SSL en local, voir l'installation ici : [mkcert](https://github.com/FiloSottile/mkcert)

### Https sur votre serveur avec Certbot

```console
# archlinux
sudo pacman -S certbot certbot-apache

# ubuntu (without snap)
sudo apt install certbot python3-certbot-apache
```

### Https sur votre serveur avec Certbot et OVH API

Si vous souhaitez utiliser l'API OVH pour la génération de vos certificats, sinon passez cette étape. Suivez d'abord **Https sur votre serveur avec Certbot**.

```console
# archlinux
sudo pacman -S certbot-dns-ovh

# ubuntu (without snap)
sudo apt install python3-certbot-dns-ovh

# pour communiquer avec OVH
pip install ovh
```

Connectez-vous à [OVH API Token](https://www.ovh.com/auth/api/createToken) et créez un paire de clés API.

```console
GET /me
GET /domain/zone/
GET /domain/zone/<your-domain>/*
PUT /domain/zone/<your-domain>/*
POST /domain/zone/<your-domain>/*
DELETE /domain/zone/<your-domain>/*
```

le fichier `.ovh.ini` contient des identifiants de connexion pour générer des alias
le fichier `.ovhapi` est utilisé par certbot pour générer les certificats ssl

copiez les modèles de ces deux fichiers et remplissez les puis déplacez ces fichiers dans `/etc/ovh`.

```
cp .ovh.ini.dist .ovh.ini
cp .ovhapi.dist .ovhapi
sudo make install-credentials
```

## Désinstallation

```console
sudo make uninstall
sudo -H pip uninstall inquirer ovh

```

## Utilisation

```console
sudo a2mksite new-site.localhost
sudo a2rmsite new-site.localhost

a2lssites

ovh-alias add new-site.<your-domain>.com server.<your-domain>.com
```
