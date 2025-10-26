import os
from pathlib import Path
import unicodedata
import pdfplumber
import csv
import datetime
import pandas as pd
import numpy as np

input_folder = Path("./sendToRaw/files/")
output_folder = Path("./processed_data")
output_folder.mkdir(parents=True, exist_ok=True)


def remove_accents(text):
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

def pdf_to_csv(input_file, output_file):
    print(f"Processando PDF -> CSV: {input_file}")
    with pdfplumber.open(input_file) as pdf, open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            for line in lines:
                line = line.replace("*", "").replace('"', "")
                parts = line.split()
                if (
                    parts
                    and parts[0].isalpha()
                    and len(parts) > 4
                    and parts[0].lower() != "consumo"
                    and parts[-5].lower() != "frigobar"
                ):
                    aparelho = remove_accents(" ".join(parts[:-5]))
                    potencia = parts[-5]
                    dias = parts[-4]
                    utilizacao = "1" if parts[-3] == "-" else parts[-3]
                    medida = "h" if parts[-2] == "-" else parts[-2]
                    consumo = parts[-1]
                    writer.writerow([aparelho, potencia, dias, utilizacao, medida, consumo])
    print(f"✔ Arquivo salvo em {output_file}")

def tratar_csv(input_file, output_file):
    print(f"Processando CSV: {input_file}")
    if not Path(input_file).exists():
        print(f"❌ Arquivo não encontrado: {input_file}")
        return
    
    try:
        df = pd.read_csv(input_file, encoding='latin1', sep=';')
    except Exception as e:
        print(f"❌ Erro ao ler {input_file}: {e}")
        return
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    nomes_padronizados = [
        'DATA',
        'HORA_UTC',
        'TEMP_MAX_HORA_ANT_C',
        'TEMP_MIN_HORA_ANT_C',
        'UMID_REL_AR_PCT',
        'DIRECAO_VENTO_GRAUS',
        'VELOC_VENTO_MS'
    ]
    if len(df.columns) == len(nomes_padronizados):
        df.columns = nomes_padronizados

    def tratar_numero(valor):
        if isinstance(valor, str):
            valor = valor.strip().replace(',', '.')
            if valor.startswith('.'):
                valor = '0' + valor
            if valor.endswith('.'):
                valor = valor + '0'
            if valor == '':
                return np.nan
            try:
                return str(float(valor))
            except ValueError:
                return valor
        return valor

    df = df.applymap(tratar_numero)
    df = df.dropna()
    df.to_csv(output_file, index=False, header=True, sep=';')


def normalizar_datahora_pld(input_file, output_file):
    print(f"Normalizando datas em {input_file}")
    df = pd.read_csv(input_file, delimiter=';')
    df['DIA'] = df['DIA'].apply(lambda x: f"{int(x):02d}")
    df['HORA'] = df['HORA'].apply(lambda x: f"{int(x):02d}")
    df['DATAHORA'] = df.apply(
        lambda row: datetime.datetime.strptime(
            f"{row['MES_REFERENCIA']}{row['DIA']}{row['HORA']}", "%Y%m%d%H"
        ),
        axis=1
    )
    df.drop(columns=['MES_REFERENCIA', 'DIA', 'HORA'], inplace=True)
    df.to_csv(output_file, index=False, header=True, sep=';')
    print(f"✔ Arquivo salvo em {output_file}")


def process_consumo_aparelho():
    input_file = input_folder / "consumoAparelho.pdf"
    output_file = output_folder / "consumo_aparelho_processed.csv"
    pdf_to_csv(input_file, output_file)

def process_pld():
    input_file = input_folder / "horarioPrecoDiff.csv"
    output_file = output_folder / "horario_preco_diff_processed.csv"
    normalizar_datahora_pld(input_file, output_file)

def process_dado_clima():
    input_file = input_folder / "clima.csv"
    output_file = output_folder / "dado_clima_processed.csv"
    tratar_csv(input_file, output_file) 


if __name__ == "__main__":
    #process_consumo_aparelho()
    #process_pld()
    process_dado_clima()
    print("All files processed and saved.")
