import os
import requests
import zipfile
from playwright.sync_api import sync_playwright

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Caminho para a pasta "arquivos" (um nível acima de web_scraping)
pasta_arquivos = os.path.join('..', 'arquivos')

# Garante que a pasta exista (se não quiser criar automaticamente, remova esta linha)
os.makedirs(pasta_arquivos, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')
    url1 = page.locator('a[data-mce-href="resolveuid/85adaa3de5464d8aadea11456bfb4f94"]').get_attribute('href')
    print(url1)

    # Aqui criamos outra página, mas você poderia reaproveitar a mesma se preferir
    page = browser.new_page()
    page.goto('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')
    url2 = page.locator('a[data-mce-href="resolveuid/85adaa3de5464d8aadea11456bfb4f94"]').get_attribute('href')
    print(url2)
    browser.close()

# Define os caminhos completos dos arquivos (dentro de "arquivos")
pdf1_path = os.path.join(pasta_arquivos, 'anexo_I.pdf')
pdf2_path = os.path.join(pasta_arquivos, 'anexo_II.pdf')
zip_path = os.path.join(pasta_arquivos, 'anexos.zip')

# Baixa os dois PDFs
download_pdf(url1, pdf1_path)
download_pdf(url2, pdf2_path)

# Cria o arquivo ZIP na mesma pasta "arquivos"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write(pdf1_path, arcname='anexo_I.pdf')
    zipf.write(pdf2_path, arcname='anexo_II.pdf')

# Remove os PDFs, deixando somente o ZIP na pasta "arquivos"
os.remove(pdf1_path)
os.remove(pdf2_path)
