import pandas as pd

# Read data from text file
with open('convert.txt', 'r') as file:
    lines = file.readlines()

# Extracting data
data = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("2024"):  # Check if line starts with a date-time format
        date_time_speed = line
        speed_parts = date_time_speed.split('- Speed: ')
        if len(speed_parts) == 2:
            date_time = speed_parts[0].strip()
            speed = speed_parts[1].strip()
            date, time = date_time.split(' ')
            # Append date, time, speed, and empty strings for latitude and longitude
            data.append([date, time, speed, '', ''])
            i += 1  # Move to the next line for latitude-longitude
        else:
            print("Date-time-speed line format is unexpected:", line)
    elif line.startswith(", Latitude:"):  # Check if line starts with a latitude-longitude format
        latitude = line.split(',')[1].split(':')[1].strip()
        longitude = line.split(',')[2].split(':')[1].strip()
        # Append latitude and longitude to the last entry in the data list
        if data:  # Check if data list is not empty
            data[-1][-2:] = [latitude, longitude]
        else:
            print("Latitude-longitude line found without preceding date-time-speed line.")
        i += 1  # Move to the next date-time-speed line
    else:
        print("Line format is unexpected:", line)
        i += 1  # Move to the next line

# Creating DataFrame
df = pd.DataFrame(data, columns=['Date', 'Time', 'Speed', 'Latitude', 'Longitude'])

# Write data to Excel file
df.to_excel('output.xlsx', index=False)  # Change 'output.xlsx' to your desired Excel file name
