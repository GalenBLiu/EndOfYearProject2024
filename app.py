from flask import Flask, request, render_template, jsonify
from datetime import datetime
from meteostat import Point, Daily
import requests
from clib import get_params, get_tavg
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

    s, tmin, tmax = get_params()
    tavg = get_tavg(pd.to_datetime('today').normalize())
    print(s, tmin, tmax, tavg)

    sc = pickle.load(open('StandardScaler-distance-holidays.pkl', 'rb'))
    # predict_data = np.array([s[0], tmin[0], tmax[0], tavg])
    predict_data = np.array([0, -12, -2, -10])
    predict_data = np.array(sc.transform(predict_data.reshape(1,-1)))

    dtc = pickle.load(open('lr_model_distance_holidays.sav', 'rb'))
    prob = dtc.predict_proba(predict_data)
    out = dtc.predict(predict_data)
    
    if (out == 1):
        s = 'Snow day!'
    elif (out == 0):
        s = 'No snow day :('
    elif (out == 2):
        s = 'Delay'
    elif (out == 3):
        s = 'Half day'
    return jsonify({'prob' : prob, 'snow_day' : s})

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/historical_prediction', methods=['GET'])
# def historical_prediction():