import enum
from datetime import datetime
from ..Services.Status import StatusProject

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()



class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    turma = Column(String(50), nullable=False)
    curso = Column(String(100), nullable=False)
    numero = Column(String(30), unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projetos = relationship("Projeto", back_populates="aluno", cascade="all, delete-orphan")


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    numero = Column(String(30), unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projetos = relationship("Projeto", back_populates="professor")
    feedbacks = relationship("Feedback", back_populates="professor", cascade="all, delete-orphan")
    prazos = relationship("PrazoAtualizacao", back_populates="professor", cascade="all, delete-orphan")


class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=False)
    imagem_projeto = Column(Text, nullable=True)
    estado = Column(Enum(StatusProject), default=StatusProject.EM_ANALISE, nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    aluno = relationship("Aluno", back_populates="projetos")
    professor = relationship("Professor", back_populates="projetos")
    atualizacoes = relationship("Atualizacao", back_populates="projeto", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="projeto", cascade="all, delete-orphan")
    prazos = relationship("PrazoAtualizacao", back_populates="projeto", cascade="all, delete-orphan")


class Atualizacao(Base):
    __tablename__ = "atualizacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(Text, nullable=False)
    imagem_atualizacao = Column(Text, nullable=True)
    data_submissao = Column(DateTime, default=datetime.utcnow)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)

    projeto = relationship("Projeto", back_populates="atualizacoes")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    comentario = Column(Text, nullable=False)
    data_feedback = Column(DateTime, default=datetime.utcnow)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)

    projeto = relationship("Projeto", back_populates="feedbacks")
    professor = relationship("Professor", back_populates="feedbacks")


class PrazoAtualizacao(Base):
    __tablename__ = "prazos_atualizacao"

    id = Column(Integer, primary_key=True, index=True)
    descricao_entrega = Column(Text, nullable=False)
    data_limite = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)

    projeto = relationship("Projeto", back_populates="prazos")
    professor = relationship("Professor", back_populates="prazos")


# configs to creste db

engine = create_engine("sqlite:///cafgest.db", echo=True)

def start_db():
    Base.metadata.create_all(bind=engine)