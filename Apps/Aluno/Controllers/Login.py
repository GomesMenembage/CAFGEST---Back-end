from fastapi import HTTPException, depends
from sqlalchemy.orm import Session
from Apps.Aluno.Schemas.AuthSchema import UserLogin
from Models.Database import Aluno
from Middleware.hash import verify_password
from Middleware.jwt import create_access_token


def login_aluno(session: Session = Depends(create_session), data: UserLogin):

    aluno = (
        session.query(Aluno).filter(Aluno.numero == numero).first()
    )

    if not aluno:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    senha_valida = verify_password(data.senha,aluno.senha)

    if not senha_valida:
        raise HTTPException(
            status_code=401,
            detail="credenciais inválidas"
        )

    token = create_access_token({
        "id": aluno.id,
        "numero": aluno.numero,
        "tipo": "aluno"
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }