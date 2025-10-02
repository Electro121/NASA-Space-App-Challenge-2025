import requests
import pandas as pd
from datetime import datetime, timedelta

# NASA POWER API base URL
POWER_BASE_URL = "https://power.larc.nasa.gov/api/v2/temporal/daily/point"

def fetch_power_data(lat, lon, start_date, end_date, parameters="PRECTOTCORR,T2M"):
    """
    Fetch daily climate data from NASA POWER API.
    Parameters: PRECTOTCORR (precipitation), T2M (temperature)
    """
    params = {
        "parameters": parameters,
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON"
    }
    response = requests.get(POWER_BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['properties']['parameter'])
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        return df
    else:
        print(f"Error fetching POWER data: {response.status_code}")
        return None

def fetch_smap_soil_moisture(lat, lon, date):
    """
    Mock SMAP soil moisture data. In real implementation, use NSIDC API.
    Returns soil moisture percentage.
    """
    # Simulate based on season or random
    # For Bangladesh, average soil moisture around 30-50%
    import random
    return random.uniform(30, 50)

def fetch_modis_ndvi(lat, lon, date):
    """
    Mock MODIS NDVI data. NDVI ranges from -1 to 1, healthy vegetation >0.3
    """
    import random
    return random.uniform(0.2, 0.8)

# Example usage
if __name__ == "__main__":
    lat, lon = 23.8103, 90.4125  # Dhaka, Bangladesh
    start = datetime.now() - timedelta(days=30)
    end = datetime.now()
    df = fetch_power_data(lat, lon, start, end)
    print(df.head())