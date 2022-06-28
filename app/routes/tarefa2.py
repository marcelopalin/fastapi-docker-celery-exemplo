try:
    from datetime import datetime, timedelta

    from celery.result import AsyncResult
    from fastapi import APIRouter, HTTPException
    from termcolor import colored
    from app.core.operacoes_matematicas import subtract
    from pprint import pprint

    from datetime import datetime
    from typing import Optional
    from pydantic import BaseModel, validator
    from app.schemas import schemas

except ImportError as error:
    print(error)
    print(f"error.name: {error.name}")
    print(f"error.path: {error.path}")



router = APIRouter(prefix="/tarefa2", tags=["Tarefa2"])


@router.post("/", status_code=201)
def run_tarefa2(payload: schemas.InfoSubtracao):
    pprint(payload, indent=2)
    task = subtract.delay(**payload.dict())
    return {"task_id": task.id}


@router.get("/status/{task_id}")
def get_status_tarefa2(task_id):
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
