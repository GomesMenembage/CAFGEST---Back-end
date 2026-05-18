from fastapi import APIRouter, Depends
from Apps.Aluno.Schemas.AuthSchema import UserRegister, UserLogin
from Apps.Aluno.Controllers.Register import criar_aluno
from Apps.Aluno.Controllers.Login import login_aluno
from sqlalchemy.orm import Session
from Services.session import create_session

auth = APIRouter(prefix="/auth", tags=["login e cadastro"])

@auth.post("/register/")
def criar_aluno(data: UserRegister, session: Session = Depends(create_session)):
    usuario = criar_aluno(data, session)
    if not usuario:
        return {"message": "Usuário já existe"}
    return usuario

@auth.post("/login/")
def login(data: UserLogin, session: Session = Depends(create_session)):
    return llogin_aluno(data, session)