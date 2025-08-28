import requests
import os

def download_pdf(url, folder="files", filename="consumoAparelho.pdf"):
    filepath = os.path.join(folder, filename)
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)
    return filename

if __name__ == "__main__":
    url = "https://igce.rc.unesp.br/Home/ComissaoSupervisora-old/ConservacaodeEnergiaCICE/tabela_consumo.pdf"  # your PDF link here
    pdf_file = download_pdf(url)