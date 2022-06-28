# MICROSSERVIÇO - EXECUTA UMA TAREFA

- CONSUMER (consumer.py)
- operacoes_matematicas - WORKERS - (executa o pedido)
- GARÇON - BROKER (recebe e encaminha) - BD DE MEMÓRIA - CHAVE E VALOR - 
- CELERY - REDIS

# Criando a Rede docker

```s
docker network create web
```

# Docker para o Traefik local

```s
docker-compose -f 01-docker-compose-traefik-local.yml up -d
```


# DOCKER DO REDIS 

docker run --rm --name redis -d -p 6379:6379 redis:latest

```

```

# RODAR OS WORKERS (SERVIÇO)

- subir os workers (redis já está rodando)

celery -A <nome_do_arquivo> worker --loglevel=INFO

Ex: 

```s
celery -A core.operacoes_matematicas worker --loglevel=info --logfile=logs/worker1.log --concurrency=10 -n worker1@%h
celery -A core.operacoes_matematicas worker --loglevel=info --logfile=logs/worker2.log --concurrency=10 -n worker2@%h
```

poetry export --without-hashes -f requirements.txt > requirements.txt

# Flower

poetry add flower

```s
# Basico
celery -A core.operacoes_matematicas flower --loglevel=info

# Avançado - porta - broker
celery -A core.operacoes_matematicas flower --port=5555 --broker=redis://redis:6379/0
```


# RODANDO A APLICAÇÃO (CLIENTE)

```s

```

# RODANDO O PAINEL Flower



