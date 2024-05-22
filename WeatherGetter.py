from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
<<<<<<< Updated upstream
start = datetime(2018, 1, 1)
end = datetime(2018, 1, 2)
print(type(start))
=======
startingHour = 0;
endingHour = 0;

start = datetime(2024, 5, 21, 12)
end = datetime(2024, 5, 21, 18)

>>>>>>> Stashed changes
# Create Point for Vancouver, BC
vancouver = Point(49.2497, -123.1193, 70)

# Get daily data for 2018
data = Daily(vancouver, start, end)
data = data.fetch()
<<<<<<< Updated upstream
=======
print(str(data))
>>>>>>> Stashed changes

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])
print(type(data))
print(data.head())
# plt.show()