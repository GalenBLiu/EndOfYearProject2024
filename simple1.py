# Simple script to check if the average temp is lower than 0 on a given day
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

#Get time stamp data
year = int(input("What year? "))
month = int(input("What month? "))
day = int(input("What day? "))

ts = datetime(year, month, day)

#Start and end are the same because 1 day only
start = end = ts

#Define location using coordinates
academies = Point(40.90243696271137, -74.0344921768194)
data = Daily(academies, start, end)

#Fetch data in pd Dataframe
data = data.fetch()
avg_temp = data.at[ts, 'tavg']
print(avg_temp)

#If average temp on the day is < 0, FREEZING!

