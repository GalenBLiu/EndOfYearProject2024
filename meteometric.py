import datetime as dt
import meteomatics.api as api

username = 'bca_ye_nick'
password = '7307BwWdQa'

coordinates = [(40.90243696271137, -74.0344921768194)]
parameters = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms']
model = 'mix'
startdate = dt.datetime.now().replace(hour=2,minute=0, second=0, microsecond=0)
enddate = startdate + dt.timedelta(days=1)
interval = dt.timedelta(hours=1)

df = api.query_time_series(coordinates, startdate, enddate, interval, parameters, username, password, model=model)
print(df.head())