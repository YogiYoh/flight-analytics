
import requests 
import csv
from pathlib import Path
import zipfile
# NOAA is for weather conditions
# TranStats - For status of flights in airports 


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
YEAR = 2026


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
        if response.status_code == 404:
            print(f"File not available yet: {url}")
            return False
        
        print(f"HTTP error: {error}")
        print("The file was not downloaded.")
        
        raise 

    except requests.exceptions.Timeout:
        print("The request timed out.")
        return False

    except requests.exceptions.ConnectionError:
        print("Could not connect to the website.")
        return False

    except requests.exceptions.RequestException as error:
        print(f"Download failed: {error}")
        return False

def extract_zip(zip_path, output_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        
        print(f"Extracting to: {output_folder}")
        
        zip_ref.extractall(output_folder)

        print(f"Extracted to: {output_folder}")
        
        

def delete_zip_files(folder_path):
    folder = Path(folder_path)

    for zip_file in folder.glob("*.zip"):
        zip_file.unlink()
        print(f"Deleted: {zip_file.name}")

with open(f"{ROOT}/csv/airport_weather_station_map.csv", "r", encoding="utf-8") as file: 
    reader = csv.DictReader(file)
    
    for row in reader:
        station_id = row["station_id"]
        airport_code = row["airport_code"]
        url = f"https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/access/by-year/2026/parquet/GHCNh_{station_id}_{YEAR}.parquet"
        output_path = f"{DATA_DIR}/GHCNh_{station_id}_2026.parquet"
        
        print(f"Donwloading {airport_code}'s NOAA weather data")
        download_file(url, output_path)
    
    for i in range(1, 13):
        url = f"https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{YEAR}_{i}.zip"
        output_path = f"{DATA_DIR}/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{YEAR}_{i}.zip"
        
        print(f"Donwloading BTS on-time performance for {YEAR}-{i:02d}")
        if download_file(url, output_path):
            extract_zip(output_path, DATA_DIR)
        
        delete_zip_files(DATA_DIR)
    
        
        
