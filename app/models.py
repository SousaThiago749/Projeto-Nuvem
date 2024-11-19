# app/models.py

from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr
from db import Base

# Modelo SQLAlchemy para o banco de dados
class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

# Modelos Pydantic para validação
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str
