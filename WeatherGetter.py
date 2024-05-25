from datetime import datetime
import matplotlib.pyplot as plt
from meteometric import Point, Daily

# Set time period
start = datetime(2018, 1, 1)
end = datetime(2018, 1, 2)
print(type(start))
# Create Point for Vancouver, BC
vancouver = Point(49.2497, -123.1193, 70)

# Get daily data for 2018
data = Daily(vancouver, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])
print(type(data))
print(data.head())
# plt.show()