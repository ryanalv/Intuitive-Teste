# Use uma imagem base do Python
FROM python:3.10

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instale o PostgreSQL e psycopg2
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
RUN pip install psycopg2-binary

# Copie o restante do código do aplicativo
COPY . .

# Copie o arquivo .env
COPY .env .env

# Exponha a porta do PostgreSQL
EXPOSE 5432

# Comando para iniciar o PostgreSQL e o script de inicialização do banco de dados
CMD ["sh", "-c", "service postgresql start && sleep 5 && python ./database/init_db.py"]