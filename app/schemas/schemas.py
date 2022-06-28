"""
    Description:

    - Pydantic Schemas

    Author:           @Palin
    Created:          2022-01-10
    Copyright:        (c) Ampere Consultoria Ltda
"""


from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class Informacao(BaseModel):
    x: Optional[int] = 10
    y: Optional[int] = 1
    url: Optional[str] = "http://google.com.br"
    data: Optional[str] = f"{datetime.today()}"
    dir_output: Optional[str] = "saida"

    @validator("data", pre=True)
    def valida_data(cls, v):
        if isinstance(v, str):
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError as err:
                raise ValueError("ERRO: data inválida. Formato: YYYY-MM-DD")
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "x": 10,
                "y": 1,
                "url": "http://google.com.br",
                "data": f"{datetime.now().strftime('%Y-%m-%d')}",
                "dir_output": "saida",
            }
        }

class InfoSubtracao(BaseModel):
    x: Optional[int] = 100
    y: Optional[int] = 20

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "x": 100,
                "y": 20,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
