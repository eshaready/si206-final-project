import csv
import sqlite3

# reads monthly average data from averaged_by_month.csv multiple times and 
# writes to the monthly averages table in the database

def write_monthly_data_to_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('bell.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist with month as INTEGER PRIMARY KEY
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_averages (
            month INTEGER PRIMARY KEY,
            tempmax REAL,
            tempmin REAL,
            temp REAL,
            precip REAL
        )
    ''')
    
    # Read data from averaged_by_month.csv and insert into the database
    inserted_rows = 0
    with open('averaged_by_month.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO monthly_averages (month, tempmax, tempmin, temp, precip)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['month'], row['tempmax'], row['tempmin'], row['temp'], row['precip']))
            if cursor.rowcount > 0:
                inserted_rows += 1
            if inserted_rows >= 12: # stop after 12 months of data
                break
    # Commit changes, and close the connection
    conn.commit()
    conn.close()

# Call the function to insert data into the database
write_monthly_data_to_db()
