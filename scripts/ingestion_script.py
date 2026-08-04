
import requests 
import csv
from pathlib import Path
# NOAA is for weather conditions
# TranStats - For status of flights in airports 


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# Station ID - Use to fetch info of weather in NOAA 
# Given each station_id in airport_weather_station_map.csv... fetch weather information up to June (2026)

def download_file(url, output_path):
    try:
        with requests.get(url, stream=True, timeout=(10, 60)) as response:
            response.raise_for_status()
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        print(f"Downloaded successfully at: {output_path}")
        return True
    
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
        print("The file was not downloaded.")
        return False

    except requests.exceptions.Timeout:
        print("The request timed out.")
        return False

    except requests.exceptions.ConnectionError:
        print("Could not connect to the website.")
        return False

    except requests.exceptions.RequestException as error:
        print(f"Download failed: {error}")
        return False
        

with open(f"{ROOT}/csv/airport_weather_station_map.csv", "r", encoding="utf-8") as file: 
    reader = csv.DictReader(file)
    
    for row in reader:
        station_id = row["station_id"]
        url = f"https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/2026/parquet/GHCNh_{station_id}_2026.parquet"
        output_path = f"{DATA_DIR}/GHCNh_{station_id}_2026.parquet"
        print(f"Donwloading {station_id}........")
        download_file(url, output_path)
        
