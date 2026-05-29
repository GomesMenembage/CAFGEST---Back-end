from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


class ProjectCreateSchema(BaseModel):
    nome: str
    descricao: str


class ProjectUpdateSchema(BaseModel):
    status: str
