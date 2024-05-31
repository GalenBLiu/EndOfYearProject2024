import requests

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
        'units': 'standard',  # Optional: 'metric' or 'standard'
        'limit': 1000  # You can adjust the limit based on your needs
    }
    
    response = requests.get(BASE_URL + 'data', headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage
station_id = 'GHCND:USW00094728'  
start_date = '2020-01-01'
end_date = '2020-05-31'
datatype_id = 'TMIN'

#US1NJBG0043 - Maywood *
#US1NJBG0064 - Wood Ridge
#USW00094728 - Central Park NY
#US1NJBG0003 - Tenafly
#US1NJBG0018 - Pal Park
#USW00094741 - Teterboro airport

historical_data = get_historical_data(station_id, start_date, end_date, datatype_id)

print(historical_data)

# # Print out the historical data
if historical_data:
    for record in historical_data['results']:
        print(f"Date: {record['date']}, {record['datatype']}: {record['value']} {record.get('units', '')}")

