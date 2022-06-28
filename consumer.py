from xml.dom.minidom import Identified
from app.core.operacoes_matematicas import add, subtract
from celery.result import AsyncResult
import asyncio

from pprint import pprint
import time

def main():
    print("Iniciando o Cliente/Consumer...")
    pedido_somar() # Bloqueante
    pedido_subtrair()

def pedido_somar():
    print("Iniciando o Cliente/Consumer solicitando uma soma...")
    payload = {"x": 1, "y": 10}
    task = add.delay(**payload)
    print(f"ID da Task {task.id}")
    task_result = AsyncResult(task.id)
    res = {
        "task_id": task.id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    print(type(res['task_status']))
    print(res['task_status'])

    while not task_result.ready():
        time.sleep(2)
        if task_result.successful():
            print("Sucesso Terminei a Tarefa")
            task_result = AsyncResult(task.id)
            res = {
                "task_id": task.id,
                "task_status": task_result.status,
                "task_result": task_result.result
            }
            pprint(res, indent=4)
        else:
            print("Continue esperando Worker Trabalhando!!")
            pprint(res, indent=2)

def pedido_subtrair():
    print("Iniciando o Cliente/Consumer solicitando uma subtração...")
    payload = {"x": 21, "y": 5}
    task = subtract.delay(**payload)
    print(f"ID da Task Subtração {task.id}")
    task_result = AsyncResult(task.id)
    res = {
        "task_id": task.id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    print(type(res['task_status']))
    print(res['task_status'])

    while not task_result.ready():
        time.sleep(2)
        if task_result.successful():
            print("Sucesso Terminei a Tarefa")
            task_result = AsyncResult(task.id)
            res = {
                "task_id": task.id,
                "task_status": task_result.status,
                "task_result": task_result.result
            }
            pprint(res, indent=4)
        else:
            print("Continue esperando Worker Trabalhando na Subtração!!")
            pprint(res, indent=2)


if __name__ == "__main__":
    main()