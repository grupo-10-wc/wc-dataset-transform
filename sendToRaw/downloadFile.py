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
    """Fetch hourly climate data for São Paulo from six months before `dia` until `dia`.

    The function uses the free Open-Meteo API to retrieve hourly values and maps
    them to the expected columns (or close equivalents):

    - DATA: YYYY-MM-DD date part of the timestamp
    - HORA_UTC: HH:MM UTC time part
    - TEMP_MAX_HORA_ANT_C: temperature (deg C) — provided as hourly temperature
    - TEMP_MIN_HORA_ANT_C: temperature (deg C) — provided as hourly temperature
    - UMID_REL_AR_PCT: relative humidity (%)
    - DIRECAO_VENTO_GRAUS: wind direction (degrees)
    - VELOC_VENTO_MS: wind speed (m/s)

    The CSV is saved to `os.path.join(folder, filename)` and the function returns
    that filepath on success. On failure it raises an exception.
    """
    # ensure dia is a datetime
    if not isinstance(dia, datetime.datetime):
        try:
            dia = pd.to_datetime(dia)
        except Exception:
            dia = datetime.datetime.now()

    # compute start date = six months before `dia`
    try:
        start = (pd.to_datetime(dia) - pd.DateOffset(months=6)).date()
    except Exception:
        # fallback to 180 days
        start = (pd.to_datetime(dia) - pd.Timedelta(days=180)).date()

    end = pd.to_datetime(dia).date()

    # São Paulo coordinates (approx.)
    latitude = -23.5505
    longitude = -46.6333

    # request hourly temperature, humidity, wind speed and direction in UTC
    # Use the archive API for historical data
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join([
            "temperature_2m",
            "relativehumidity_2m",
            "windspeed_10m",
            "winddirection_10m",
        ]),
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "timezone": "UTC",
    }

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    try:
        resp = requests.get(base_url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch climate data: {e}")

    hourly = data.get("hourly")
    if not hourly:
        raise RuntimeError("No hourly data returned from API")

    # convert to DataFrame
    df = pd.DataFrame(hourly)

    # `time` column is ISO timestamps in UTC
    if "time" not in df.columns:
        raise RuntimeError("API response missing 'time' values")

    df["time"] = pd.to_datetime(df["time"])  # UTC
    # build required columns
    df_out = pd.DataFrame()
    df_out["DATA"] = df["time"].dt.date.astype(str)
    df_out["HORA_UTC"] = df["time"].dt.strftime("%H:%M")

    # map temperature and humidity/wind fields if present
    if "temperature_2m" in df.columns:
        # we don't have intra-hour min/max; provide hourly temperature as both
        df_out["TEMP_MAX_HORA_ANT_C"] = df["temperature_2m"]
        df_out["TEMP_MIN_HORA_ANT_C"] = df["temperature_2m"]
    else:
        df_out["TEMP_MAX_HORA_ANT_C"] = pd.NA
        df_out["TEMP_MIN_HORA_ANT_C"] = pd.NA

    if "relativehumidity_2m" in df.columns:
        df_out["UMID_REL_AR_PCT"] = df["relativehumidity_2m"]
    else:
        df_out["UMID_REL_AR_PCT"] = pd.NA

    if "winddirection_10m" in df.columns:
        df_out["DIRECAO_VENTO_GRAUS"] = df["winddirection_10m"]
    else:
        df_out["DIRECAO_VENTO_GRAUS"] = pd.NA

    if "windspeed_10m" in df.columns:
        df_out["VELOC_VENTO_MS"] = df["windspeed_10m"]
    else:
        df_out["VELOC_VENTO_MS"] = pd.NA

    # save to CSV
    df_out.to_csv(filepath, index=False)
    return filepath


    
if __name__ == "__main__":
    download("https://igce.rc.unesp.br/Home/ComissaoSupervisora-old/ConservacaodeEnergiaCICE/tabela_consumo.pdf", "consumoAparelho.pdf")
    download("https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content", "horarioPrecoDiff.csv")
    get_clima(datetime.datetime.now(), "clima.csv")
