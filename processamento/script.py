import os
import requests
from datetime import datetime
import zipfile
from bs4 import BeautifulSoup

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Arquivo {filename} baixado com sucesso.")

def listar_arquivos(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.zip')]

def baixar_arquivos():
    # Obtém a data atual e subtrai dois anos
    data_atual = datetime.now()
    ano_subtraido = data_atual.year - 2

    # URL base do repositório
    base_url = 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'

    # Lista de anos a partir do ano subtraído até o ano atual
    anos = list(range(ano_subtraido, data_atual.year + 1))

    # Diretório para salvar os arquivos baixados
    download_dir = './arquivos'
    os.makedirs(download_dir, exist_ok=True)

    for ano in anos:
        # URL da pasta do ano
        ano_url = f"{base_url}{ano}/"
        # Lista de arquivos na pasta do ano
        arquivos = listar_arquivos(ano_url)

        for arquivo in arquivos:
            arquivo_url = f"{ano_url}{arquivo}"
            download_file(arquivo_url, os.path.join(download_dir, arquivo))

def descompactar_arquivos():
    # Diretório onde os arquivos ZIP foram baixados
    download_dir = './arquivos'

    # Lista todos os arquivos no diretório
    for item in os.listdir(download_dir):
        if item.endswith('.zip'):
            file_path = os.path.join(download_dir, item)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            print(f"Arquivo {item} descompactado com sucesso.")

baixar_arquivos()
descompactar_arquivos()