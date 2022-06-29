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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "x": 10,
                "y": 1,
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
