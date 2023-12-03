import requests
from bs4 import BeautifulSoup as bs
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('box_office.db')
cursor = conn.cursor()

# Recreate the table with a composite UNIQUE constraint
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TopMonthlyReleases (
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
        raise Exception(f'Failed to load page {url}')
    return bs(response.text, 'html.parser')

def get_box_office_info(tr_tag, month):
    year, title, gross = None, None, None
    # Extracting the year
    year_tag = tr_tag.find('td', class_="a-text-left mojo-header-column mojo-truncate mojo-field-type-year mojo-sort-column")
    if year_tag:
        year = year_tag.get_text(strip=True)

    # Extracting the title
    title_tag = tr_tag.find('td', class_="a-text-left mojo-field-type-release mojo-cell-wide")
    if not title_tag:
        return None
    title = title_tag.get_text(strip=True)

    # Extracting the gross value
    gross_tag = tr_tag.find('td', class_="a-text-right mojo-field-type-money")
    if not gross_tag:
        return None
    gross = gross_tag.get_text(strip=True)

    return year, month, title, gross

def scrape_info(url, month):
    box_doc = get_box_office_page(url)
    box_office_rows = box_doc.find_all('tr')[1:13]  # Assuming the first row is not data

    for tr in box_office_rows:
        if get_box_office_info(tr, month):
            year, month, title, gross = get_box_office_info(tr, month)
            cursor.execute("SELECT id FROM TopMonthlyReleases WHERE year = ? AND month = ? AND title = ?", (year, month, title))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO TopMonthlyReleases (year, month, title, gross) VALUES (?, ?, ?, ?)", (year, month, title, gross))
            else:
                print(f"Duplicate found, not inserting: {year}, {month}, {title}")  # Debugging for duplicates
    conn.commit()

# Scrape data for each month and year
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'november', 'october', 'december']  # Extend this list to include all months
for month in months:
    url = f'https://www.boxofficemojo.com/month/{month}/?grossesOption=calendarGrosses&sort=year'
    scrape_info(url, month.capitalize())

cursor.execute("SELECT year, month, title, gross FROM TopMonthlyReleases ORDER BY year, month")
print("Top Grossing Titles Each Month (2012-2022):")
for row in cursor.fetchall():
    print(f"Year: {row[0]}, Month: {row[1]}, Title: {row[2]}, Gross: {row[3]}")

# Close the connection
conn.close()