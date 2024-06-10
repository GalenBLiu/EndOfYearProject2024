from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from clib import get_historical_data
from meteostat import Point, Daily, Stations
import time

#priority for snow:
#maywood --> tenafly --> wridge --> cenpark

cancelled_dates = ['2022-01-07', '2023-02-28', '2024-02-13']

maywood = 'GHCND:US1NJBG0043'
wridge = 'GHCND:US1NJBG0064'
cenpark = 'GHCND:USW00094728'
tenafly = 'GHCND:US1NJBG0003'
palpark = 'GHCND:US1NJBG0018'
teterboro = 'GHCND:USW00094741'
fairlawn = 'GHCND:US1NJBG0056'
glenrock = 'GHCND:US1NJBG0017'

start_date = '2024-01-01'
start_dt = pd.to_datetime(start_date, format='ISO8601')
end_date = '2024-06-03'
end_dt = pd.to_datetime(end_date, format='ISO8601')

maywood_snow = get_historical_data(maywood, start_date, end_date, 'SNOW')
palpark_snow = get_historical_data(palpark, start_date, end_date, 'SNOW')
wridge_snow = get_historical_data(wridge, start_date, end_date, 'SNOW')
tenafly_snow = get_historical_data(tenafly, start_date, end_date, 'SNOW')
time.sleep(1)
cenpark_snow = get_historical_data(cenpark, start_date, end_date, 'SNOW')
cenpark_tmin = get_historical_data(cenpark, start_date, end_date, 'TMIN')
cenpark_tmax = get_historical_data(cenpark, start_date, end_date, 'TMAX')
teterboro_snow = get_historical_data(teterboro, start_date, end_date, 'SNOW')
time.sleep(1)
fairlawn_snow = get_historical_data(fairlawn, start_date, end_date, 'SNOW')
glenrock_snow = get_historical_data(glenrock, start_date, end_date, 'SNOW')

if maywood_snow:
    maywood_snow_dates = [record['date'] for record in maywood_snow['results']]
if palpark_snow:
    palpark_snow_dates = [record['date'] for record in palpark_snow['results']]
if wridge_snow:
    wridge_snow_dates = [record['date'] for record in wridge_snow['results']]
if tenafly_snow:
    tenafly_snow_dates = [record['date'] for record in tenafly_snow['results']]
if cenpark_snow:
    cenpark_snow_dates = [record['date'] for record in cenpark_snow['results']]
if cenpark_tmin:
    cenpark_tmin_dates = [record['date'] for record in cenpark_tmin['results']]
if cenpark_tmax:
    cenpark_tmax_dates = [record['date'] for record in cenpark_tmax['results']]
if teterboro_snow:
    teterboro_snow_dates = [record['date'] for record in teterboro_snow['results']]
if fairlawn_snow:
    fairlawn_snow_dates = [record['date'] for record in fairlawn_snow['results']]
if glenrock_snow:
    glenrock_snow_dates = [record['date'] for record in glenrock_snow['results']]

def check_weekend(date):
    if date.dayofweek > 4:
        return True

dates_weekends = []

for date in pd.date_range(start=start_dt, end=end_dt, freq='D'):
    dates_weekends.append(date)

dates = []
for date in dates_weekends:
    if not check_weekend(date):
        date_string = date.strftime('%Y-%m-%d') 
        dates.append(date_string)

def get_tavg(ts):
    start = end = ts
    academies = Point(40.90243696271137, -74.0344921768194)
    data = Daily(academies, start, end)
    data = data.fetch()
    return data.at[ts, 'tavg']

snow = []
tmin = []
tmax = []
tavg = []
cancelled = []
for date in dates:
    datestr = date+'T00:00:00'

    if date in cancelled_dates:
        cancelled.append(1)
    else:
        cancelled.append(0)

    snows = []

    try:
        snows.append(maywood_snow['results'][maywood_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(palpark_snow['results'][palpark_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(tenafly_snow['results'][tenafly_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(wridge_snow['results'][wridge_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(cenpark_snow['results'][cenpark_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(teterboro_snow['results'][teterboro_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(fairlawn_snow['results'][fairlawn_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)
    try:
        snows.append(glenrock_snow['results'][glenrock_snow_dates.index(datestr)]['value'])
    except Exception:
        snows.append(0)

    snow.append(max(snows))

    try:
        tmin.append(cenpark_tmin['results'][cenpark_tmin_dates.index(datestr)]['value'])
    except ValueError:
        tmin.append(float('nan'))
    
    try:
        tmax.append(cenpark_tmax['results'][cenpark_tmax_dates.index(datestr)]['value'])
    except ValueError:
        tmax.append(float('nan'))

    tavg.append(get_tavg(pd.to_datetime(date, format='%Y-%m-%d')))

print(len(snow))
print(len(tmin))
print(len(tmax))
print(len(tavg))

data = {'Date': dates, 'Snow': snow, 'Tmin': tmin, 'Tmax': tmax, 'Tavg': tavg, 'Snow Day':cancelled}
df = pd.DataFrame(data)

print(df)
df.to_csv(f'{start_date}-{end_date}.csv')

# columns = ['mass_1_source', 'mass_2_source', 'luminosity_distance', 'chi_eff', 
#       'total_mass_source', 'chirp_mass_source', 'redshift', 'far', 'p_astro', 'final_mass_source'] 

# data = cl.iterativelyImpute('181entries.csv', dropMarginal=True)

# y = data.GPS
# X = data[columns]
# trainX, valX, trainy, valy = train_test_split(X, y, random_state=1, shuffle=True)
# for nodes in [2,3,4,5,40,50,60,70,80,90]:
#     model = RandomForestRegressor(max_leaf_nodes=nodes, random_state=1)
#     model.fit(trainX, trainy)
#     preds_val = model.predict(valX)
#     print(preds_val)
#     print(valy.head())
#     mae = mean_absolute_error(valy, preds_val)
#     print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(nodes, mae))