
import pdb
import datetime
import requests
import pandas as pd
from io import StringIO

# TODO: SUBSTITUIR ESSA LEITURA PELA LEITURA NO S3

def read_from_raw(
    save_date:datetime.datetime=datetime.datetime.now()
):
    res = requests.get("https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content")
    res.raise_for_status()
    
    texto = res.text
    
    return texto

def teste():
    texto = read_from_raw()
    df = pd.read_csv(StringIO(texto), delimiter=';')
    pdb.set_trace()
    df['DIA']
    df['datahora'] = df['MES_REFERENCIA'].astype(str) + df['DIA'].astype(str) + df['HORA'].astype(str)
    return df

if __name__ == "__main__":
    teste()