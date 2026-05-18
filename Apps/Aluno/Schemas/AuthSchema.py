from pydantic import BaseModel

UserRegister(BaseModel):
    nome: str
    email:str
    turma:str
    numero:str
    senha:str