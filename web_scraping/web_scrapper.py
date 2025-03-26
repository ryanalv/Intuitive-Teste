from playwright.sync_api import sync_playwright
import requests
import zipfile
import os

# Function to download a PDF
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Open the browser and click the links of the attachments
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')
    variavelA = page.locator('a[data-mce-href="resolveuid/f710899c6c7a485ea62a1acc75d86c8c"]')
    page.locator('a[data-mce-href="resolveuid/85adaa3de5464d8aadea11456bfb4f94"]')
    browser.close()

# Download the PDFs
for url, filename in zip(pdf_urls, pdf_filenames):
    download_pdf(url, filename)

# Create a ZIP file containing the downloaded PDFs
zip_filename = "../arquivos/Anexos.zip"
with zipfile.ZipFile(zip_filename, 'w') as zip_file:
    for filename in pdf_filenames:
        zip_file.write(filename)

# Clean up the downloaded PDF files, if necessary
for filename in pdf_filenames:
    os.remove(filename)