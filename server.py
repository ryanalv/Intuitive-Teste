# server.py
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Carregar o CSV em um DataFrame
df = pd.read_csv('operadoras_de_plano_de_saude_ativas.csv')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        return jsonify(results.to_dict(orient='records'))
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)