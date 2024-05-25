import requests

API_TOKEN = 'VLVtaEUDWkLeHsqoCNJaTiDFYqZHRMGd'
BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

def get_historical_data(station_id, start_date, end_date):
    headers = {
        'token': API_TOKEN
    }
    params = {
        'datasetid': 'GHCND',  # Global Historical Climatology Network - Daily
        # 'datatypeid': 'SNWD',
        'stationid': station_id,
        'startdate': start_date,
        'enddate': end_date,
        'units': 'standard',  # Optional: 'metric' or 'standard'
        'limit': 1000  # You can adjust the limit based on your needs
    }
    
    response = requests.get(BASE_URL + 'datatypes', headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
station_id = 'GHCND:US1NJBG0064'  # Example: Central Park, NY, US
start_date = '2024-01-10'
end_date = '2024-02-28'

historical_data = get_historical_data(station_id, start_date, end_date)

print(historical_data)

# # Print out the historical data
# if historical_data:
#     for record in historical_data['results']:
#         print(f"Date: {record['date']}, {record['datatype']}: {record['value']} {record.get('units', '')}")

