import csv
import sqlite3
from collections import defaultdict
from datetime import datetime

# creates an average_by_year csv file and writes the data to the average by year table in database
def average_by_year():
    # Initialize dictionaries to store yearly data, with each year having the following dict as default value
    yearly_data = defaultdict(lambda: {'tempmax': [], 'tempmin': [], 'temp': [], 'precip': []})

    # Read data from each CSV file
    for year in range(2012, 2023):
        filename = f"{year}.csv"
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date = datetime.strptime(row['datetime'], '%Y-%m-%d')
                year_key = date.year
                yearly_data[year_key]['tempmax'].append(float(row['tempmax']))
                yearly_data[year_key]['tempmin'].append(float(row['tempmin']))
                yearly_data[year_key]['temp'].append(float(row['temp']))
                yearly_data[year_key]['precip'].append(float(row['precip']))

    # Calculate the yearly averages
    averaged_data = []
    for year, values in sorted(yearly_data.items()):
        avg_tempmax = sum(values['tempmax']) / len(values['tempmax'])
        avg_tempmin = sum(values['tempmin']) / len(values['tempmin'])
        avg_temp = sum(values['temp']) / len(values['temp'])
        avg_precip = sum(values['precip']) / len(values['precip'])
        averaged_data.append({'year': year, 'tempmax': avg_tempmax, 'tempmin': avg_tempmin, 'temp': avg_temp, 'precip': avg_precip})

    # Write the results to a new CSV file named averaged_by_year.csv
    with open('averaged_by_year.csv', 'w', newline='') as csvfile:
        fieldnames = ['year', 'tempmax', 'tempmin', 'temp', 'precip']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in averaged_data:
            writer.writerow(row)

    conn = sqlite3.connect('bell.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist with year as INTEGER PRIMARY KEY
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yearly_averages (
            year INTEGER PRIMARY KEY,
            tempmax REAL,
            tempmin REAL,
            temp REAL,
            precip REAL
        )
    ''')

    # Insert data into the table
    for row in averaged_data:
        cursor.execute('''
            INSERT OR IGNORE INTO yearly_averages (year, tempmax, tempmin, temp, precip)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['year'], row['tempmax'], row['tempmin'], row['temp'], row['precip']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

average_by_year()