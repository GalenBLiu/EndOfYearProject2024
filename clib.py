import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from meteostat import Point, Daily
import time

API_TOKEN = 'VLVtaEUDWkLeHsqoCNJaTiDFYqZHRMGd'
BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

def get_historical_data(station_id, start_date, end_date, datatypeid):
    headers = {
        'token': API_TOKEN
    }
    params = {
        'datasetid': 'GHCND',  # Global Historical Climatology Network - Daily
        'datatypeid': datatypeid,
        'stationid': station_id,
        'startdate': start_date,
        'enddate': end_date,
        'units': 'metric',  # Optional: 'metric' or 'standard'
        'limit': 1000  # You can adjust the limit based on your needs
    }
    
    response = requests.get(BASE_URL + 'data', headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_params():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 40.90243696271137,
        "longitude": -74.0344921768194,
        "daily": ["temperature_2m_max", "temperature_2m_min", "snowfall_sum"],
        "timezone": "America/New_York",
        "forecast_days": 2
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["snowfall_sum"] = daily_snowfall_sum

    return daily_snowfall_sum, daily_temperature_2m_min, daily_temperature_2m_max

def get_tavg(ts):
    start = end = ts
    academies = Point(40.90243696271137, -74.0344921768194)
    data = Daily(academies, start, end)
    data = data.fetch()
    return data.at[ts, 'tavg']

def conditions_of_day(s):
    maywood = 'GHCND:US1NJBG0043'
    wridge = 'GHCND:US1NJBG0064'
    cenpark = 'GHCND:USW00094728'
    tenafly = 'GHCND:US1NJBG0003'
    palpark = 'GHCND:US1NJBG0018'
    teterboro = 'GHCND:USW00094741'
    fairlawn = 'GHCND:US1NJBG0056'
    glenrock = 'GHCND:US1NJBG0017'

    date = pd.to_datetime(s, format='ISO8601')
    if date.dayofweek > 4:
        raise ValueError('Weekend!')

    maywood_snow = get_historical_data(maywood, s, s, 'SNOW')
    palpark_snow = get_historical_data(palpark, s, s, 'SNOW')
    wridge_snow = get_historical_data(wridge, s, s, 'SNOW')
    tenafly_snow = get_historical_data(tenafly, s, s, 'SNOW')
    time.sleep(1)
    cenpark_snow = get_historical_data(cenpark, s, s, 'SNOW')
    cenpark_tmin = get_historical_data(cenpark, s, s, 'TMIN')
    cenpark_tmax = get_historical_data(cenpark, s, s, 'TMAX')
    teterboro_snow = get_historical_data(teterboro, s, s, 'SNOW')
    time.sleep(1)
    fairlawn_snow = get_historical_data(fairlawn, s, s, 'SNOW')
    glenrock_snow = get_historical_data(glenrock, s, s, 'SNOW')

    if maywood_snow:
        maywood_snow_val = maywood_snow['results'][0]['value']
    if palpark_snow:
        palpark_snow_val = palpark_snow['results'][0]['value']
    if wridge_snow:
        wridge_snow_val = wridge_snow['results'][0]['value']
    if tenafly_snow:
        tenafly_snow_val = tenafly_snow['results'][0]['value']
    if cenpark_snow:
        cenpark_snow_val = cenpark_snow['results'][0]['value']
    if cenpark_tmin:
        cenpark_tmin_val = cenpark_tmin['results'][0]['value']
    if cenpark_tmax:
        cenpark_tmax_val = cenpark_tmax['results'][0]['value']
    if teterboro_snow:
        teterboro_snow_val = teterboro_snow['results'][0]['value']
    if fairlawn_snow:
        fairlawn_snow_val = fairlawn_snow['results'][0]['value']
    if glenrock_snow:
        glenrock_snow_val = glenrock_snow['results'][0]['value']
    
    snow = 0
    tmin = 0
    tmax = 0
    tavg = 0

    try:
        snow = maywood_snow_val
    except Exception:
        try:
            snow = teterboro_snow_val
        except Exception:
            try:
                snow = palpark_snow_val
            except Exception:
                try:
                    snow = tenafly_snow_val
                except Exception:
                    try:
                        snow = wridge_snow_val
                    except Exception:
                        try:
                            snow = fairlawn_snow_val
                        except Exception:
                            try:
                                snow = glenrock_snow_val
                            except Exception:
                                try:
                                    snow = cenpark_snow_val
                                except Exception:
                                    snow = 0

    try:
        tmin = cenpark_tmin_val
    except ValueError:
        tmin = 0

    try:
        tmax = cenpark_tmax_val
    except ValueError:
        tmax = 0

    tavg = get_tavg(date)
    return snow, tmin, tmax, tavg
