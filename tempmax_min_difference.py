import csv
import sqlite3

def calculate_temp_difference():

    # Read data from averaged_by_year.csv
    with open('averaged_by_year.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    conn = sqlite3.connect('bell.db')
    cursor = conn.cursor()

    # Create a new table if it doesn't exist with year as INTEGER PRIMARY KEY
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temp_difference (
            year INTEGER PRIMARY KEY,
            temp_difference REAL
        )
    ''')

    # Calculate differences and insert into the temp_difference table
    for row in data:
        year = int(row['year'])
        tempmax = float(row['tempmax'])
        tempmin = float(row['tempmin'])
        temp_difference = tempmax - tempmin

        cursor.execute('''
            INSERT OR IGNORE INTO temp_difference (year, temp_difference)
            VALUES (?, ?)
        ''', (year, temp_difference))

    conn.commit()
    conn.close()

calculate_temp_difference()