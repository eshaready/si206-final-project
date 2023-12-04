import requests
from bs4 import BeautifulSoup as bs
import sqlite3

#Finished
# Connect to SQLite database
conn = sqlite3.connect('box_office.db')
cursor = conn.cursor()

# Recreate the table with a composite UNIQUE constraint
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TopMonthlyReleases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        month INTEGER,
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
            m = month_string_to_int(month)
            cursor.execute("SELECT id FROM TopMonthlyReleases WHERE year = ? AND month = ? AND title = ?", (int(year), m, title))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO TopMonthlyReleases (year, month, title, gross) VALUES (?, ?, ?, ?)", (int(year), m, title, gross))
            else:
                print(f"Duplicate found, not inserting: {year}, {m}, {title}")  # Debugging for duplicates
    conn.commit()

def month_string_to_int(month):
    if month == "January":
        return 1
    if month == "February":
        return 2
    if month == "March":
        return 3
    if month == "April":
        return 4
    if month == "May":
        return 5
    if month == "June":
        return 6
    if month == "July":
        return 7
    if month == "August":
        return 8
    if month == "September":
        return 9
    if month == "October":
        return 10
    if month == "November":
        return 11
    if month == "December":
        return 12

# Scrape data for each month and year
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'november', 'october', 'december']  # Extend this list to include all months

month = input("Choose a month to gather data for (lowercase, full month name):")
url = f'https://www.boxofficemojo.com/month/{month}/?grossesOption=calendarGrosses&sort=year'
scrape_info(url, month.capitalize())

cursor.execute("SELECT year, month, title, gross FROM TopMonthlyReleases WHERE month = ? ORDER BY year, month", (month_string_to_int(month.capitalize()),))
print("Top Grossing Titles Each Month (2012-2022):")
for row in cursor:
    print(f"Year: {row[0]}, Month: {row[1]}, Title: {row[2]}, Gross: {row[3]}")

# Close the connection
conn.close()