import requests
import os

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
        
        filepath = os.path.join(folder, 'dadoClima.csv')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        return filename
        
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
        return None
    except IOError as e:
        print(f"File write error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    
