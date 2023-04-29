#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROJECT_DIR=$(dirname "$SCRIPT_DIR")
REMOTE_PATH=/home/htavernier/vhost-builder

rsync -av --delete \
  -e "ssh -p 276" \
  --exclude __pycache__ \
  --exclude .local \
  $PROJECT_DIR/ \
  htavernier@vps1.server.bric-network.com:$REMOTE_PATH

scp -P 276 $PROJECT_DIR/.local/configuration.arch.ini \
  htavernier@vps1.server.bric-network.com:$REMOTE_PATH/configuration.ini

ssh -p 276 htavernier@vps1.server.bric-network.com "sudo -- sh -c '\
  cd $REMOTE_PATH && make install'"

# for python ovh
scp -P 276 $PROJECT_DIR/.local/.bric-network.ovh.ini htavernier@vps1.server.bric-network.com:~/.ovh.ini

# certbot
scp -P 276 $PROJECT_DIR/.local/.bric-network.ovhapi htavernier@vps1.server.bric-network.com:~/.ovhapi

ssh -p 276 htavernier@vps1.server.bric-network.com "sudo -- sh -c '\
  chmod 644 .ovh.ini && \
  chmod 600 .ovhapi && \
  mkdir -p /etc/ovh && \
  mv .ovhapi /etc/ovh && \
  mv .ovh.ini /etc/ovh && \
  chown root:root /etc/ovh/.ovh.ini && \
  chown root:root /etc/ovh/.ovhapi'"