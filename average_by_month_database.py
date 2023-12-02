import csv
import sqlite3
from collections import defaultdict
from datetime import datetime

# Initialize dictionaries to store monthly data
monthly_data = defaultdict(lambda: {'tempmax': [], 'tempmin': [], 'temp': [], 'precip': []})

for year in range(2012, 2023):
    filename = f"{year}.csv"
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row['datetime'], '%Y-%m-%d')
            month_key = int(f"{date.year}{date.month:02d}")
            monthly_data[month_key]['tempmax'].append(float(row['tempmax']))
            monthly_data[month_key]['tempmin'].append(float(row['tempmin']))
            monthly_data[month_key]['temp'].append((float(row['tempmax']) + float(row['tempmin'])) / 2)  # Calculate average temperature
            monthly_data[month_key]['precip'].append(float(row['precip']))

# Calculate the monthly averages
averaged_data = []
for month, values in sorted(monthly_data.items()):
    avg_tempmax = sum(values['tempmax']) / len(values['tempmax'])
    avg_tempmin = sum(values['tempmin']) / len(values['tempmin'])
    avg_temp = sum(values['temp']) / len(values['temp'])
    avg_precip = sum(values['precip']) / len(values['precip'])
    averaged_data.append({'month': month, 'tempmax': avg_tempmax, 'tempmin': avg_tempmin, 'temp': avg_temp, 'precip': avg_precip})

conn = sqlite3.connect('bell.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS monthly_averages (
        month INTEGER PRIMARY KEY,
        tempmax REAL,
        tempmin REAL,
        temp REAL,
        precip REAL
    )
''')

# Insert data into the table
for row in averaged_data:
    cursor.execute('''
        INSERT INTO monthly_averages (month, tempmax, tempmin, temp, precip)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['month'], row['tempmax'], row['tempmin'], row['temp'], row['precip']))

conn.commit()
conn.close()
