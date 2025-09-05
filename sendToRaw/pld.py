import os
import requests
import datetime
from exportFile import send_to_s3

def upload_raw_data(
    save_date:datetime.datetime=datetime.datetime.now()
):
    res = requests.get("https://pda-download.ccee.org.br/korJMXwpSLGyVlpRMQWduA/content")

    texto = res.text
    now = save_date.strftime("%Y-%m-%d")
    save_path = f"./raw/{now}"
    os.makedirs(save_path, exist_ok=True)
    with open(f"{save_path}/pld.csv", "w") as f:
        f.write(texto)

    send_to_s3(save_path)