from fastapi import HTTPException
from sqlalchemy.orm import Session, Depends
from Services.session import create_session
from Models.database import Aluno
from Apps.Aluno.Schemas.AuthSchema import UserRegister
from Middleware.hash import hash_password


def criar_aluno(session: Session = Depends(create_session), data: UserRegister):

    aluno_existente =session.query(Aluno).filter(Aluno.numero == numero).first()

    if aluno_existente:

        raise HTTPException(status_code=400,detail="Número já cadastrado")

    aluno = Aluno(nome=data.nome,turma=data.turma,curso=data.curso, numero=data.numero,senha=hash_password(data.senha))

    session.add(aluno)
    session.commit()
    session.refresh(aluno)

    return {

        "message":"Aluno criado",

    }