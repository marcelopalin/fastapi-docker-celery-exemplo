# Executando tudo pelo Docker

Como estamos rodando o container com o usuário ubuntu
e não root, tive que adpatar a saída dos Logs.

Então, certifique-se de executar os passos abaixo antes:

```s
sudo mkdir logs
sudo chown -R ubuntu:ubuntu logs
sudo chmod a+rwx logs
```

Execute o `init_config.sh` mas antes descomente as linhas abaixo
caso seja necessário conforme explicação:

O Container criado utiliza o usuário `ubuntu` e caso você esteja implantando o projeto
no seu Windows WSL será necessário executar as linhas abaixo para criarmos

```s
sudo groupadd -g 1000 ubuntu
sudo useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo,ubuntu -u 1000 ubuntu
```

As linhas abaixo criar uma pasta para armazenar os dados do BD de forma permanente
caso precise reconstruir o container

```s
mkdir -p $HOME/.docker/database/{dump_clima_passado,proj-celery-exemplo_data}
sudo chown -R ubuntu:ubuntu $HOME/.docker/database/dump_clima_passado
sudo chown -R ubuntu:ubuntu $HOME/.docker/database/proj-celery-exemplo_data
```

Agora basta subir os contâiners:

```s
docker-compose up -d
```

## Executando Manualamente

Subindo o serviço de Broker: sugestão é subir o `redis` utilizando docker com a opção --rm que quando parar
o container é removido.

```s
 docker run --rm -d --name redis redis:6-alpine
```

Antes, verifique a pasta `logs`, se tiver arquivos dentro faça:

```s
 ls -lah
total 32K
drwxrwxrwx  2 ubuntu ubuntu 4.0K Jun 26 23:39 .
drwxr-xr-x 15 mpi    mpi    4.0K Jun 27 08:27 ..
-rw-r--r--  1   1002 root   9.1K Jun 27 14:23 api-clima-passado.log
-rw-r--r--  1   1002 root   8.9K Jun 27 14:22 worker1.log

Removendo-os:
$ sudo rm -rf *
```

## Backend FastAPI

`http://localhost:8000/docs`

```s
uvicorn app.main:app --port 8000 --reload
```

## BD Postgres e PGAdmin4

Subindo o container fora da rede `web`. Caso precise subir dentro da rede coloque a opção: `--network=web`.
Se for uma máquina nova que não tem a rede docker chamada `web` execute o comando: `docker network create web`.

```s
docker run --rm --name postgres -e "POSTGRES_USER=postgres" -e "POSTGRES_DB=fastapi_exemplo_db" -e "POSTGRES_PASSWORD=secret" -p 5432:5432 -v ~/.docker/database/proj-celery-exemplo_data:/var/lib/postgresql/data/ -d postgres:13.1
```

Subindo PGAdmin o container fora da rede `web`. Caso precise subir dentro da rede coloque a opção: `--network=web`.

```s
docker run --rm --name pgadmin -p 16543:80 -e "PGADMIN_DEFAULT_EMAIL=admin@mail.com" -e "PGADMIN_DEFAULT_PASSWORD=secret" -d dpage/pgadmin4
```

Acesse o PGADMIN na porta `http://localhost:16543`

Crie Registre o servidor utilizando:
Name= Nome Qualquer = pg_local
host = postgres
user = postgres
password = secret

Utilizando o Alembic para gerar as Tabelas do BD. Como o backend foi rodado manualmente
vamos rodar as migrations manualmente também.

Obs: se já havia rodado o projeto antes, provavelmente o BD e as tabelas
já foram criados. Como comopartilhamos os volumes, os dados não devem ter se perdido.

```s
alembic upgrade head
```

## Subindo o Worker (Producer)

Verifique se subiu o container do `redis`:
Subindo o serviço de Broker: sugestão é subir o `redis` utilizando docker com a opção --rm que quando parar
o container é removido.

```s
 docker run --rm -d --name redis -p 6379:6379 redis:6-alpine
```

Pronto, podemos subir os workers:

```s
poetry shell
celery -A app.workers.operacoes_matematicas worker --loglevel=info --logfile=logs/worker1.log
```

## Subindo o Flower

```s
celery -A app.workers.operacoes_matematicas flower --port=5555 --broker=redis://localhost:6379/0
```

## Frontend

Na pasta `frontend` temos um Html simples para mostrar a utilização do retorno do celery.

## Documetação do Projeto com Mkdocs

Suba a documentação com o comando:

```s
mkdocs serve -a localhost:8001 --livereload
```
