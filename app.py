from flask import Flask, request, render_template, jsonify
from datetime import datetime
from meteostat import Point, Daily
import requests
from clib import get_params, get_tavg, conditions_of_day
import pickle
import numpy as np
import pandas as pd

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
@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

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

@app.route('/get_forecast', methods=['GET'])
def get_12h():
    base_url = "https://api.weather.gov/points/40.90243696271137,-74.0344921768194"
    response = requests.get(base_url)
    x = response.json()
    forecast_url = x['properties']['forecast']
    print(forecast_url)
    r = requests.get(forecast_url)
    forecast = r.json()
    tavg = forecast['properties']['periods'][0]['temperature']
    img_url = forecast['properties']['periods'][0]['icon']
    detailed_forecast = forecast['properties']['periods'][0]['detailedForecast']
    print(detailed_forecast)
    return jsonify({'tavg' : tavg, 'img_url': img_url, 'description': detailed_forecast})


@app.route('/current_weather', methods=['GET'])
def current_weather():
    s, tmin, tmax = get_params()
    tavg = get_tavg(pd.to_datetime('today').normalize())
    print(s, tmin, tmax, tavg)

    sc = pickle.load(open('StandardScaler-distance-holidays.pkl', 'rb'))
    predict_data = np.array([s[0], tmin[0], tmax[0], tavg])
    predict_data = np.array(sc.transform(predict_data.reshape(1,-1)))

    lr = pickle.load(open('lr_model_distance_holidays.sav', 'rb'))
    prob = lr.predict_proba(predict_data)[0]
    out = lr.predict(predict_data)
    a = 0
    b = 0
    c = 0
    d = 0
    a = round(prob[1]*100, 1)
    b = round(prob[0]*100,1)
    c = round(prob[2]*100,1)
    d = round(prob[3]*100,1)

    if (out == 1):
        s = 'Snow day!'
    elif (out == 0):
        s = 'No snow day :('
    elif (out == 2):
        s = 'Delay!'
    elif (out == 3):
        s = 'Half day!'

    return jsonify({'probSchool' : b, 'probClose':a, 'probDelay':c, 'probHalf':d, 'snow_day' : s})

@app.route('/historical_weather', methods=['POST'])
def historical_weather():
    data = request.json
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    ts = datetime(year, month, day)
    date = ts.strftime('%Y-%m-%d') 
    sc = pickle.load(open('inflated.pkl', 'rb'))
    try:
        predict_data = np.array(conditions_of_day(date))
    except:
        return jsonify({'probSchool' : 0, 'probClose':100, 'probDelay':0, 'probHalf':0, 'snow_day' : s})

    predict_data = np.array(sc.transform(predict_data.reshape(1,-1)))
    lr = pickle.load(open('inflated.sav', 'rb'))
    prob = lr.predict_proba(predict_data)[0]
    out = lr.predict(predict_data)
    a = 0
    b = 0
    c = 0
    d = 0
    a = round(prob[1]*100, 1)
    b = round(prob[0]*100,1)
    c = round(prob[2]*100,1)
    d = round(prob[3]*100,1)

    if (out == 1):
        s = 'Snow day!'
    elif (out == 0):
        s = 'No snow day :('
    elif (out == 2):
        s = 'Delay!'
    return jsonify({'probSchool' : b, 'probClose':a, 'probDelay':c, 'snow_day' : s})

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/historical_prediction', methods=['GET'])
# def historical_prediction():