from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://intuitive:1234@localhost:5432/teste_intuitive')
Base = declarative_base()