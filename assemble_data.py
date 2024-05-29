from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from clib import get_historical_data
from datetime import datetime
from meteostat import Point, Daily, Stations

#priority for snow:
#maywood --> tenafly --> wridge --> cenpark

cancelled_dates = ['2022-01-07', '2023-02-28', '2024-02-13']

maywood = 'GHCND:US1NJBG0043'
wridge = 'GHCND:US1NJBG0064'
cenpark = 'GHCND:USW00094728'
tenafly = 'GHCND:US1NJBG0003'

start_date = '2024-01-01'
start_dt = pd.to_datetime(start_date, format='ISO8601')
end_date = '2024-05-27'
end_dt = pd.to_datetime(end_date, format='ISO8601')

maywood_snow = get_historical_data(maywood, start_date, end_date, 'SNOW')
wridge_snow = get_historical_data(wridge, start_date, end_date, 'SNOW')
tenafly_snow = get_historical_data(tenafly, start_date, end_date, 'SNOW')
cenpark_snow = get_historical_data(cenpark, start_date, end_date, 'SNOW')
cenpark_tmin = get_historical_data(cenpark, start_date, end_date, 'TMIN')
cenpark_tmax = get_historical_data(cenpark, start_date, end_date, 'TMAX')

maywood_snow_dates = [record['date'] for record in maywood_snow['results']]
wridge_snow_dates = [record['date'] for record in wridge_snow['results']]
tenafly_snow_dates = [record['date'] for record in tenafly_snow['results']]
cenpark_snow_dates = [record['date'] for record in cenpark_snow['results']]
cenpark_tmin_dates = [record['date'] for record in cenpark_tmin['results']]
cenpark_tmax_dates = [record['date'] for record in cenpark_tmax['results']]

dates = []
for date in pd.date_range(start=start_dt, end=end_dt, freq='D'):
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

    try:
        snow.append(maywood_snow['results'][maywood_snow_dates.index(datestr)]['value'])
    except ValueError:
        try:
            snow.append(tenafly_snow['results'][tenafly_snow_dates.index(datestr)]['value'])
        except ValueError:
            try:
                snow.append(wridge_snow['results'][wridge_snow_dates.index(datestr)]['value'])
            except ValueError:
                try:
                    snow.append(cenpark_snow['results'][cenpark_snow_dates.index(datestr)]['value'])
                except ValueError:
                    snow.append(float('nan'))
    
    try:
        tmin.append(cenpark_tmin['results'][cenpark_tmin_dates.index(datestr)]['value'])
    except ValueError:
        tmin.append(float('nan'))
    
    try:
        tmax.append(cenpark_tmax['results'][cenpark_tmax_dates.index(datestr)]['value'])
    except ValueError:
        tmax.append(float('nan'))

    tavg.append(get_tavg(pd.to_datetime(date, format='%Y-%m-%d')))

print(snow)
print(tmin)
print(tmax)
print(tavg)

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