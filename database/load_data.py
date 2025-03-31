import os
from sqlalchemy.orm import Session
from database.config import SessionLocal, engine
from database.models import Tabela1, Tabela2

def load_data():
    session = SessionLocal()
    try:
        # Iterar e carregar dados nos modelos Tabela1 e Tabela2
        # Exemplo de inserção de dados
        tabela1_data = Tabela1(nome="Exemplo1")
        tabela2_data = Tabela2(descricao="Exemplo2")
        session.add(tabela1_data)
        session.add(tabela2_data)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    load_data()