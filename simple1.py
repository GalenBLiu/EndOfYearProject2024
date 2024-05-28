# Simple script to check if the average temp is lower than 0 on a given day
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Stations, Hourly

#Get time stamp data
year = int(input("What year? "))
month = int(input("What month? "))
d = int(input("What day? "))

ts = datetime(year, month, d, hour=0)

#Start and end are the same because 1 day only
start = ts
print(start)
end = ts.replace(hour=23)
print(end)



#Define location using coordinates
stations = Stations()
stations = stations.nearby(40.90243696271137, -74.0344921768194)
station = stations.fetch(1)
print(station)
academies = Point(40.90243696271137, -74.0344921768194)
data = Hourly('KTEB0', start, end)
print(data.coverage())

#Fetch data in pd Dataframe
data = data.fetch()
print(data)
# avg_temp = data.at[ts, 'tavg']
# snow = data.at[ts, 'snow']
# print("avg_temp:" + str(avg_temp))
# print('snow:' + str(snow))

# print(data.loc[:, 'snow'])
for x in data.index:
    print(x)
    print(data.loc[x, 'snow'])

#If average temp on the day is < 0, FREEZING!

