from pydantic import BaseModel

class UserRegister(BaseModel):
    nome: str
    curso: str
    turma:str
    numero:str
    senha:str
    
class UserLogin(BaseModel):
    numero: str
    turma: str
    senha: str
    