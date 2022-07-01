#!/bin/bash
cp .env_example .env
cp .secrets_example.toml .secrets.toml
cp settings.local.example.toml settings.local.toml
docker network create web_exemplo
sudo mkdir logs
mkdir -p $HOME/.docker/database/{dump_fastapi_docker_celery_examplo,fastapi_docker_celery_examplo_data}
# sudo chown -R ubuntu:ubuntu $HOME/.docker/database/dump_fastapi_docker_celery_examplo
# sudo chown -R ubuntu:ubuntu $HOME/.docker/database/fastapi_docker_celery_examplo_data
