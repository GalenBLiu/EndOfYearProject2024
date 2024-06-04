from flask import Flask, request, render_template, jsonify
from datetime import datetime
from meteostat import Point, Daily
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/report')
def report():
    return render_template('report.html')
@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/get_temperature', methods=['POST'])
def get_temperature():
    data = request.json
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    
    ts = datetime(year, month, day)
    start = end = ts
    academies = Point(40.90243696271137, -74.0344921768194)
    data = Daily(academies, start, end)

    data = data.fetch()
    avg_temp = data.at[ts, 'tavg']
    s = ''
    if avg_temp < 0:
        s = 'Snow day!'
    else:
        s = 'No snow day :('

    return jsonify({'tavg' : avg_temp, 'snow_day' : s})

@app.route('/current_weather', methods=['GET'])
def current_weather():
    base_url = "https://api.weather.gov/points/40.90243696271137,-74.0344921768194"

    response = requests.get(base_url)

    x = response.json()

    forecast_url = x['properties']['forecast']
    print(forecast_url)

    r = requests.get(forecast_url)
    forecast = r.json()
    
    avg_24 = (forecast['properties']['periods'][0]['temperature'] + forecast['properties']['periods'][2]['temperature'])/2
    s = ''
    if (avg_24 < 0):
        s = 'Snow day!'
    else:
        s = 'No snow day :('
    return jsonify({'tavg' : avg_24, 'snow_day' : s})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/historical_prediction', methods=['GET'])
def historical_prediction():
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=ST&limit=52"

    response = requests.get(base_url)