#!/bin/bash
cp .env_example .env
cp .secrets_example.toml .secrets.toml
cp settings.local.example.toml settings.local.toml
docker network create web_exemplo
sudo mkdir logs
sudo chown -R ubuntu:ubuntu logs
sudo chmod a+rwx logs
# Para compartilhar os volumes com o container no WSL2
# Obs: provavelmente no servidor o usuario e grupo ubuntu já existirão - então comente as próximas 2 linhas
# sudo groupadd -g 1002 ubuntu
# sudo useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo,ubuntu -u 1001 ubuntu
# https://phoenixnap.com/kb/create-directory-linux-mkdir-command
mkdir -p $HOME/.docker/database/{dump_proj-celery-exemplo,proj-celery-exemplo_data}
sudo chown -R ubuntu:ubuntu $HOME/.docker/database/dump_proj-celery-exemplo
sudo chown -R ubuntu:ubuntu $HOME/.docker/database/proj-celery-exemplo_data
