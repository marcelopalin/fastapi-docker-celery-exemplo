from typing import Optional
from pydantic import BaseModel

class Info(BaseModel):
    a: Optional[int] = 10
    b: Optional[int] = 1
    z: Optional[int] = 1
    url: Optional[str] = "google.com"

dados_recebidos_pydantic = Info(x=10, y=20)
dicionario_puro = {'a':1, 'b':2}


def somar(a=0, b=0, c=0):
    return a + b + c

print("Unpacking Dicionario Puro")
resp = somar(**dicionario_puro)
print(f"A soma dos dados do Dicionario: {resp}")

resp = somar(**dados_recebidos_pydantic.dict())
print(f"A soma dos dados do Pydantic: {resp}")

print(dados_recebidos_pydantic.dict())
