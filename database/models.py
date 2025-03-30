from sqlalchemy import Column, Integer, String
from .config import Base

class Tabela1(Base):
    __tablename__ = 'tabela1'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)

class Tabela2(Base):
    __tablename__ = 'tabela2'
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)