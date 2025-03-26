import os
import zipfile
import tempfile
import pdfplumber
import pandas as pd

def make_unique_columns(header):
    """Cria cabeçalhos únicos para as colunas."""
    seen = set()
    unique_header = []
    for col in header:
        col = col or 'Unnamed'
        if col in seen:
            count = 1
            new_col = f"{col}_{count}"
            while new_col in seen:
                count += 1
                new_col = f"{col}_{count}"
            col = new_col
        seen.add(col)
        unique_header.append(col)
    return unique_header

def is_header_row(row, header_model):
    """Verifica se a linha é igual ao cabeçalho modelo."""
    return all(cell in header_model for cell in row)

def clean_list(lst):
    """Limpa a lista removendo espaços em branco e convertendo para minúsculas."""
    return [str(item).strip().lower() for item in lst]

# Configurações de caminho
zip_path = os.path.join('..', 'arquivos', 'anexos.zip')  # Arquivo ZIP na pasta "arquivos"
pdf_filename = 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf'  # Nome correto do PDF a ser processado
csv_filename = os.path.join('..', 'arquivos', 'rol_procedimentos.csv')  # Nome do CSV a ser gerado na pasta "arquivos"
zip_final = os.path.join('..', 'arquivos', 'Teste_ryan_alves.zip')  # Nome do ZIP final na pasta "arquivos"

# Verifica se o arquivo ZIP existe
if not os.path.exists(zip_path):
    raise FileNotFoundError(f"O arquivo ZIP {zip_path} não foi encontrado.")

# Lista os arquivos dentro do ZIP
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_contents = zip_ref.namelist()
    print("Arquivos no ZIP:", zip_contents)
    if pdf_filename not in zip_contents:
        raise FileNotFoundError(f"{pdf_filename} não encontrado em {zip_path}")

# Cria um diretório temporário para extrair o PDF
with tempfile.TemporaryDirectory() as tmpdirname:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        print(f"Extraindo {pdf_filename} para o diretório temporário...")
        zip_ref.extract(pdf_filename, path=tmpdirname)

    pdf_path = os.path.join(tmpdirname, pdf_filename)

    all_tables = []
    header_model = None
    print(f"Processando o PDF {pdf_path} com pdfplumber...")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                print(f"Pág. {i + 1}: {len(tables)} tabela(s) encontrada(s)")
                for table in tables:
                    # Ignore tabelas sem pelo menos 2 linhas (cabeçalho + dados)
                    if len(table) <= 1:
                        continue
                    # Cria cabeçalho único e converte dados
                    header = make_unique_columns(table[0])
                    data = table[1:]
                    df = pd.DataFrame(data, columns=header)

                    # Se ainda não definimos header_model, use este; caso contrário, se a primeira linha for igual ao header_model, remova-a
                    if header_model is None:
                        header_model = header
                    else:
                        if df.shape[0] > 0 and is_header_row(list(df.iloc[0]), header_model):
                            df = df.iloc[1:]
                    # Remover colunas que sejam completamente vazias
                    df = df.dropna(axis=1, how='all')
                    all_tables.append(df)
            else:
                print(f"Pág. {i + 1}: Nenhuma tabela encontrada.")

    if not all_tables:
        raise ValueError("Nenhuma tabela foi extraída do PDF.")

    # Concatena todas as tabelas; se houver discrepância de colunas, use join='outer'
    try:
        df_combined = pd.concat(all_tables, ignore_index=True)
    except Exception as e:
        print("Erro na concatenação direta, tentando união outer:", e)
        df_combined = pd.concat(all_tables, ignore_index=True, join='outer')

    # Remover, no DataFrame concatenado, quaisquer linhas que sejam iguais ao cabeçalho (limpo)
    if header_model is not None:
        header_clean = clean_list(header_model)
        df_combined = df_combined[~df_combined.apply(lambda row: clean_list(list(row)) == header_clean, axis=1)]

    # Renomeia as colunas "OD" e "AMB" conforme a legenda
    rename_map = {
        'OD': 'Procedimentos Odontológicos',
        'AMB': 'Procedimentos Ambulatoriais'
    }
    new_columns = {}
    for col in df_combined.columns:
        base = col.split('_')[0]
        if base in rename_map:
            new_columns[col] = rename_map[base]
    if new_columns:
        df_combined.rename(columns=new_columns, inplace=True)

    # Substitui os valores das colunas "Procedimentos Odontológicos" e "Procedimentos Ambulatoriais"
    if 'Procedimentos Odontológicos' in df_combined.columns:
        df_combined['Procedimentos Odontológicos'] = df_combined['Procedimentos Odontológicos'].replace({'OD': 'Procedimentos Odontológicos'})
    if 'Procedimentos Ambulatoriais' in df_combined.columns:
        df_combined['Procedimentos Ambulatoriais'] = df_combined['Procedimentos Ambulatoriais'].replace({'AMB': 'Procedimentos Ambulatoriais'})

    print("Estrutura final do DataFrame:", df_combined.shape)
    print("Colunas:", df_combined.columns.tolist())

    # Salva o DataFrame em CSV
    print(f"Salvando os dados extraídos em {csv_filename}...")
    df_combined.to_csv(csv_filename, index=False, encoding='utf-8-sig')

# Compacta o CSV em um arquivo ZIP denominado "Teste_ryan_alves.zip"
print(f"Compactando {csv_filename} em {zip_final}...")
with zipfile.ZipFile(zip_final, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename, arcname=os.path.basename(csv_filename))

print("Processamento concluído!")