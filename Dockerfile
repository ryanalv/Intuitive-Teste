# Use uma imagem base do Python
FROM python:3.10

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do aplicativo
COPY . .

# Copie o arquivo .env
COPY .env .env

# Execute o script de inicialização do banco de dados
CMD ["python", "database/init_db.py"]