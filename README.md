# vhost-builder

Configure automatiquement vos hôtes virtuels apache.
Optimisé pour un environnement Linux, on configure les chemins vers les fichiers de configuration à l'aide du fichier `configuration.ini`.
Auto-complétion des noms de domaine avec Bash.

## Installation

nécessite d'installer globalement le package Python inquirer

```console
sudo -H pip install inquirer

sudo pacman -S mkcert
mkcert -install

make install
```

## Utilisation

```console
amksite new-site.localhost
armsite new-site.localhost
aensite new-site.localhost
adissite new-site.localhost

alssites
```