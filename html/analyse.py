import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# Function to parse each line of the file
def parse_line(line):
    parts = line.strip().split(" - ")
    timestamp = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
    data = parts[1].split(", ")
    speed = float(data[0].split(": ")[1])
    latitude = float(data[1].split(": ")[1])
    longitude = float(data[2].split(": ")[1])
    return timestamp, speed, latitude, longitude

# Function to read the file and parse each line
def read_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            timestamp, speed, latitude, longitude = parse_line(line)
            data.append((timestamp, speed, latitude, longitude))
    return data

# Function to plot speed versus time
def plot_speed_vs_time(data):
    timestamps = [record[0] for record in data]
    speeds = [record[1] for record in data]

    plt.figure(figsize=(10, 6))
    plt.scatter(timestamps, speeds, marker='o', alpha=0.5)
    plt.title('Speed vs Time')
    plt.xlabel('Time')
    plt.ylabel('Speed (m/s)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to find most common speed when driver might be sleeping
def most_common_speed_when_sleeping(data):
    # Assuming sleep time as 11:00 PM to 6:00 AM
    sleep_data = [record for record in data if 23 <= record[0].hour or record[0].hour <= 6]
    if not sleep_data:
        print("No data found during sleep hours.")
        return
    
    speeds = [record[1] for record in sleep_data]
    most_common_speed = Counter(speeds).most_common(1)[0][0]
    print("Most common speed during sleep hours:", most_common_speed)

# Main function to run the script
def main():
    filename = "convert.txt"
    data = read_file(filename)
    plot_speed_vs_time(data)
    most_common_speed_when_sleeping(data)

if __name__ == "__main__":
    main()
