import csv
import sqlite3

# reads monthly average data from averaged_by_month.csv multiple times and 
# writes to the monthly averages table in the database

def write_monthly_data_to_db():
    conn = sqlite3.connect('bell.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_averages (
            date INTEGER PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            tempmax REAL,
            tempmin REAL,
            temp REAL,
            precip REAL
        )
    ''')
    
    # Read data from averaged_by_month.csv and insert into the database
    inserted_rows = 0
    with open('weather-api/averaged_by_month.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO monthly_averages (date, year, month, tempmax, tempmin, temp, precip)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (row['date'], row['year'], row['month'], row['tempmax'], row['tempmin'], row['temp'], row['precip']))
            if cursor.rowcount > 0:
                inserted_rows += 1
            if inserted_rows >= 12: # stop after 12 months of data
                break
    conn.commit()
    conn.close()

# Call the function to insert data into the database
write_monthly_data_to_db()
