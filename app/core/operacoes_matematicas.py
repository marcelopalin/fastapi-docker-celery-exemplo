from celery import Celery
import time
from random import randrange
import os
from datetime import datetime, timedelta

# Evite utilizar app
# celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379')
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

@celery.task(name="tarefa_somar")
def add(x: int = 10, y: int = 1):
    time.sleep(12)
    return x + y

@celery.task(name="tarefa_subtrair")
def subtract(x: int, y: int):
    time.sleep(6)
    valor = randrange(1,6) # 1 a 5
    if valor < 2:
        raise Exception("Erro na Subtração! Valor < 2 provocado!!")
    return x - y