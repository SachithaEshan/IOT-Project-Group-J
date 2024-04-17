from datetime import datetime

# Function to parse time from a line
def parse_time(line):
    try:
        time = datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S').time()
        return time
    except ValueError:
        return None

# Read data from the text file and count occurrences of each hour
hour_counts = {}  # Dictionary to store counts for each hour
total_occurrences = 0
with open('drowsiness_log.txt', 'r') as file:
    for line in file:
        time = parse_time(line)
        if time:
            hour = time.hour
            if hour not in hour_counts:
                hour_counts[hour] = 0
            hour_counts[hour] += 1
            total_occurrences += 1

# Find the hour with the highest occurrence
max_hour = max(hour_counts, key=hour_counts.get)
max_occurrences = hour_counts[max_hour]

# Calculate percentage
percentage = (max_occurrences / total_occurrences) * 100

print("Hour with the most occurrences of drowsiness:", max_hour)
print("Number of occurrences:", max_occurrences)
print("Percentage of total occurrences: {:.2f}%".format(percentage))
