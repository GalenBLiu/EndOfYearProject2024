# Simple script to check if the average temp is lower than 0 on a given day
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

#Get time stamp data
year = int(input("What year? "))
month = int(input("What month? "))
d = int(input("What day? "))

ts = datetime(year, month, d)

#Start and end are the same because 1 day only
start = ts
print(start)
end = ts.replace(month=3)
print(end)



#Define location using coordinates
academies = Point(40.90243696271137, -74.0344921768194)
data = Daily(academies, start, end)

#Fetch data in pd Dataframe
data = data.fetch()
print(data)
# avg_temp = data.at[ts, 'tavg']
# snow = data.at[ts, 'snow']
# print("avg_temp:" + str(avg_temp))
# print('snow:' + str(snow))
print(data.loc[:, 'snow'])
for x in data.index:
    print(data.loc[x, 'snow'])
#If average temp on the day is < 0, FREEZING!

