from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Hourly

# Set time period
start = datetime(2024, 5, 12, 0)
end = datetime(2020, 5, 12, 20)
print(type(start))

Hackensack = Point(40.8859, -74.0435, 8)

# Get hourly data for 2018
data = Hourly(Hackensack, start, end)
data = data.fetch()
print(data)
# Plot line chart including average, minimum and maximum temperature
#data.plot(y=['tavg', 'tmin', 'tmax'])
#print(type(data))
#print(data.head())
# plt.show()