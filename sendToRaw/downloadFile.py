import os
import requests
import datetime
import pandas as pd

def download(url, filename, folder="./sendToRaw/files"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)
    return filename

def get_clima(
    dia: datetime.datetime = datetime.datetime.now(),
    filename: str="clima.csv",
    folder="./sendToRaw/files"
):
    lat = -23.5505
    lon = -46.6333
    inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(hours=24)
    fim = inicio.replace(hour=23, minute=59, second=59)
    url = "https://api.open-meteo.com/v1/forecast?past_days=2"

    def to_utc_z(dt: datetime.datetime) -> str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        else:
            dt = dt.astimezone(datetime.timezone.utc)
        return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    if inicio >= fim:
        raise ValueError("inicio deve ser anterior a fim")

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relativehumidity_2m", "windspeed_10m", "winddirection_10m"],
        "start": to_utc_z(inicio),
        "end": to_utc_z(fim),
        "timezone": "UTC"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()["hourly"]

    results = []
    for i in range(1, len(data["time"])):
        tmax = max(data["temperature_2m"][i-1], data["temperature_2m"][i])
        tmin = min(data["temperature_2m"][i-1], data["temperature_2m"][i])
        results.append({
            "DATA": data["time"][i].split("T")[0],
            "HORA_UTC": data["time"][i].split("T")[1].replace("Z",""),
            "TEMP_MAX_HORA_ANT_C": tmax,
            "TEMP_MIN_HORA_ANT_C": tmin,
            "UMID_REL_AR_PCT": data["relativehumidity_2m"][i],
            "DIRECAO_VENTO_GRAUS": data["winddirection_10m"][i],
            "VELOC_VENTO_MS": data["windspeed_10m"][i]
        })
    df = pd.DataFrame(results)
    df = df[df['DATA']==str(dia.date())].reset_index(drop=True)
    df.to_csv(os.path.join(folder, filename), index=False, header=True, sep=';')
    return df.to_dict(orient='records')


    
if __name__ == "__main__":
    download("https://igce.rc.unesp.br/Home/ComissaoSupervisora-old/ConservacaodeEnergiaCICE/tabela_consumo.pdf", "consumoAparelho.pdf")
    download("https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content", "horarioPrecoDiff.csv")
    get_clima(datetime.datetime.now(), "clima.csv")
