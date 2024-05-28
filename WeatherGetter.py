from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Hourly

# Set time period
start = datetime(2018, 3, 13, 0)
end = datetime(2018, 3, 15, 0)
print(type(start))
# Create Point for Vancouver, BC
Hackensack = Point(49.2497, -123.1193, 70)

# Get daily data for 2018
data = Hourly(Hackensack, start, end)
data = data.fetch()
print(data)
# Plot line chart including average, minimum and maximum temperature
#data.plot(y=['tavg', 'tmin', 'tmax'])
#print(type(data))
#print(data.head())
# plt.show()