from pydantic import BaseModel

UserRegister(BaseModel):
    nome: str
    curso: str
    turma:str
    numero:str
    senha:str
    
UserLogin(BaseModel):
    numero: str
    turma: str
    senha: str
    