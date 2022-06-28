from xml.dom.minidom import Identified
from app.core.operacoes_matematicas import add, subtract
from celery.result import AsyncResult
import asyncio

from pprint import pprint
import time
from random import randrange

def main():
    print("Iniciando o Cliente/Consumer...")
    pedido_somar() # NÃO BLOQUEANTE
    pedido_subtrair()

def pedido_somar():
    print("Iniciando o Cliente/Consumer solicitando uma soma...")
    payload = {"x": 1, "y": 10}
    task = add.delay(**payload)
    print(f"ID da Task {task.id}")

def pedido_subtrair():
    print("Iniciando o Cliente/Consumer solicitando uma subtração...")
    payload = {"x": 21, "y": 5}
    task = subtract.delay(**payload)
    print(f"ID da Task {task.id}")



if __name__ == "__main__":
    main()