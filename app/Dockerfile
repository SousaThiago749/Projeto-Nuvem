# app/Dockerfile

# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt e instalar as dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o conteúdo da pasta app para o diretório de trabalho no container
COPY . .

# Expor a porta em que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
