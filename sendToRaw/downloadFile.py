import os
import zipfile
import requests
from io import BytesIO

def download(url, filename, folder="./sendToRaw/files"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)
    return filename

def download_specific_zip_file(url, filename, folder="./sendToRaw/files", keep_zip=False):
    try:
        os.makedirs(folder, exist_ok=True)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            if filename in z.namelist():
                with z.open(filename) as extracted:
                    out_path = os.path.join(folder, "dadoClima.csv")
                    with open(out_path, 'wb') as out_file:
                        out_file.write(extracted.read())
                print(f"Arquivo extraído para {out_path}")
                return out_path
            else:
                print(f"Arquivo {filename} não encontrado no ZIP.")
                return None
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
        return None
    except zipfile.BadZipFile as e:
        print(f"Arquivo ZIP inválido: {e}")
        return None
    except IOError as e:
        print(f"File write error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    
if __name__ == "__main__":
    download("https://igce.rc.unesp.br/Home/ComissaoSupervisora-old/ConservacaodeEnergiaCICE/tabela_consumo.pdf", "consumoAparelho.pdf")
    download("https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content", "horarioPrecoDiff.csv")
    download_specific_zip_file("https://portal.inmet.gov.br/uploads/dadoshistoricos/2025.zip","INMET_SE_SP_A771_SAO PAULO - INTERLAGOS_01-01-2025_A_31-08-2025.CSV")
