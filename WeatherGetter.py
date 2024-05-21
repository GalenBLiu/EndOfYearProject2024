from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Hourly

# Set time period
startingHour = 0;
endingHour = 0;

start = datetime(2024, 5, 21, startingHour)
end = datetime(2024, 5, 21, endingHour)

# Create Point for Vancouver, BC
hackensack = Point(40.8838, -74.0555, 70)

# Get hourly data
data = Hourly(hackensack, start, end, 'EST', True, False)
data = data.fetch()
#print(str(data))

# Plot line chart including average, minimum and maximum temperature
#data.plot(y=['temp'])
#plt.show()
