import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import engine, Base

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)