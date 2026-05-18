from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from Apps.Aluno.Schemas.AuthSchema import UserLogin
from Models.database import Aluno
from Middleware.hash import verify_password
from Middleware.jwt import create_access_token
from Services.session import create_session

def login_aluno( data: UserLogin,session: Session = Depends(create_session)):

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