try:
    from datetime import datetime, timedelta

    from celery.result import AsyncResult
    from fastapi import APIRouter, HTTPException
    from termcolor import colored
    from app.core.operacoes_matematicas import add
    from pprint import pprint

    from datetime import datetime
    from typing import Optional
    from pydantic import BaseModel, validator
    from app.schemas import schemas

except ImportError as error:
    print(error)
    print(f"error.name: {error.name}")
    print(f"error.path: {error.path}")



router = APIRouter(prefix="/tarefa1", tags=["Tarefa1"])


@router.post("/", status_code=201)
def run_tarefa1(payload: schemas.Informacao):
    pprint(payload, indent=2)
    task = add.delay(payload.x, payload.y)
    return {"task_id": task.id}


@router.get("/status/{task_id}")
def get_status_tarefa1(task_id):
    """Chamdo de 1 em 1 segundo pelo Axios.Get
    Olhe no JS do Html do Frontend
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result


@router.get("/", include_in_schema=False)
async def index():
    """Mostra como excluir uma rota da documentação"""
    return {"message": "Rota Raiz da Tarefa 1."}
