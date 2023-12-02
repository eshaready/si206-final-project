import requests
from bs4 import BeautifulSoup as bs
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('box_office.db')
cursor = conn.cursor()

# Recreate the table with a composite UNIQUE constraint
cursor.execute('''
    CREATE TABLE TopMonthlyReleases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year TEXT,
        month TEXT,
        title TEXT,
        gross TEXT,
        UNIQUE(year, month, title)
    )
''')
conn.commit()

def get_box_office_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    return bs(response.text, 'html.parser')

def get_box_office_info(tr_tag, year, month):
    # Parsing the table row
    td_tags = tr_tag.find_all('td')
    if len(td_tags) < 7:  # Adjust based on the website's table structure
        return None

    title = td_tags[2].text.strip()
    gross = td_tags[3].text.strip()
    return year, month, title, gross

def scrape_info(url, year, month):
    box_doc = get_box_office_page(url)
    box_office_rows = box_doc.find_all('tr')[1:]

    for tr in box_office_rows:
        info = get_box_office_info(tr, year, month)
        if info:
            year, month, title, gross = info
            cursor.execute("SELECT id FROM TopMonthlyReleases WHERE year = ? AND month = ? AND title = ?", (year, month, title))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO TopMonthlyReleases (year, month, title, gross) VALUES (?, ?, ?, ?)", (year, month, title, gross))
    conn.commit()

# Scrape data for each month and year
years = range(2012, 2023)  # From 2012 to 2022
months = ['january', 'february', 'march']  # Extend this list to include all months
for year in years:
    for month in months:
        url = f'https://www.boxofficemojo.com/month/{month}/{year}/?grossesOption=calendarGrosses'
        scrape_info(url, str(year), month.capitalize())

# Close the connection
conn.close()