from flask import Flask, request, render_template, jsonify
from datetime import datetime
from meteostat import Point, Daily

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_temperature', methods=['POST'])
def get_temperature():
    data = request.json
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    
    # Define the location (example: San Francisco)
    ts = datetime(year, month, day)
    start = end = ts
    academies = Point(40.90243696271137, -74.0344921768194)
    data = Daily(academies, start, end)

    #Fetch data in pd Dataframe
    data = data.fetch()
    avg_temp = data.at[ts, 'tavg']
    s = ''
    if avg_temp < 0:
        s = 'Snow Day!'
    else:
        s = 'No snow day :('

    return jsonify({'tavg' : avg_temp, 'snow_day' : s})

if __name__ == '__main__':
    app.run(debug=True)
