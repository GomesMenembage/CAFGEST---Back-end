from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Project
from app.schemas import (
    RegisterSchema,
    LoginSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema
)

from app.security import (
    hash_password,
    verify_password
)

from app.auth import (
    create_token,
    get_current_user
)


router = APIRouter()


@router.post("/api/auth/register")
def register(
    data: RegisterSchema,
    db: Session = Depends(get_db)
):

    user_exists = db.query(User).filter(
        User.email == data.email
    ).first()

    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    user = User(
        nome=data.nome,
        email=data.email,
        senha=hash_password(data.senha)
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "Usuário criado"
    }


@router.post("/api/auth/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    if not verify_password(
        data.senha,
        user.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    token = create_token({
        "user_id": user.id
    })

    return {
        "token": token
    }


@router.get("/api/projects")
def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    projects = db.query(Project).filter(
        Project.user_id == current_user.id
    ).all()

    return projects


@router.post("/api/projects")
def create_project(
    data: ProjectCreateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    project = Project(
        nome=data.nome,
        descricao=data.descricao,
        status="PLANEJAMENTO",
        user_id=current_user.id
    )

    db.add(project)

    db.commit()

    db.refresh(project)

    return project


@router.put("/api/projects/{project_id}")
def update_project(
    project_id: int,
    data: ProjectUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado"
        )

    project.status = data.status

    db.commit()

    db.refresh(project)

    return project


@router.delete("/api/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado"
        )

    db.delete(project)

    db.commit()

    return {
        "message": "Projeto deletado"
    }
