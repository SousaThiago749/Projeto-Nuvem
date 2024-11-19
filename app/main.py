# app/main.py

from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List
import requests

from models import UsuarioCreate, UsuarioLogin, UsuarioDB
from auth_utils import criar_jwt, validar_jwt, hash_senha, verificar_senha
from db import SessionLocal, engine, Base, get_db

app = FastAPI()

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Endpoint de registro de usuário
@app.post("/registrar")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe
    db_usuario = db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Hash da senha e criação do usuário
    hashed_password = hash_senha(usuario.senha)
    usuario_db = UsuarioDB(nome=usuario.nome, email=usuario.email, senha=hashed_password)
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    
    # Gera o token JWT
    token = criar_jwt({"sub": usuario.email})
    return {"jwt": token}

# Endpoint de login
@app.post("/login")
def login(request: UsuarioLogin, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == request.email).first()
    if not usuario or not verificar_senha(request.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Gera o token JWT
    token = criar_jwt({"sub": usuario.email})
    return {"jwt": token}

# Endpoint de consulta protegida por autenticação
@app.get("/consultar")
def consultar_dados(authorization: str = Header(None, alias="Authorization")):
    # Verifica se o token foi fornecido
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token não fornecido")
    
    # Extrai o token do header
    token = authorization.split(" ")[1]
    payload = validar_jwt(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Token inválido ou expirado")
    
    # Fazer a requisição para a API do CoinDesk
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao obter dados da API externa")
    
    dados = response.json()
    
    # Processar os dados e retornar a resposta
    resultado = {
        "hora_atualizacao": dados.get("time", {}).get("updated"),
        "moeda": "USD",
        "preco_bitcoin": dados.get("bpi", {}).get("USD", {}).get("rate")
    }
    
    return resultado