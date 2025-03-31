# analytical_queries.py
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://intuitive:123456@db:5432/teste_intuitive")
engine = create_engine(DATABASE_URL)

def execute_query(query):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        for row in result:
            print(row)

# Query para o último trimestre
query_last_quarter = """
SELECT operadora, SUM(despesa) AS total_despesa
FROM despesas
WHERE categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND data >= DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '1 quarter'
GROUP BY operadora
ORDER BY total_despesa DESC
LIMIT 10;
"""

# Query para o último ano
query_last_year = """
SELECT operadora, SUM(despesa) AS total_despesa
FROM despesas
WHERE categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND data >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
GROUP BY operadora
ORDER BY total_despesa DESC
LIMIT 10;
"""

print("Top 10 operadoras no último trimestre:")
execute_query(query_last_quarter)

print("\nTop 10 operadoras no último ano:")
execute_query(query_last_year)