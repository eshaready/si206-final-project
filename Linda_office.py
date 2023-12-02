import requests
from bs4 import BeautifulSoup as bs
import sqlite3

# Connect to SQLite database 1
conn = sqlite3.connect('box_office.db')
cursor = conn.cursor()

# Create Movies table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE
    )
''')
conn.commit()

def get_box_office_page(year_url):
    response = requests.get(year_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(year_url))
    return bs(response.text, 'html.parser')

def get_box_office_info(tr_tags):
    # Find all the td tags in the tr tags
    td_tags = tr_tags.find_all('td')
    # Create variable which contains the box office information
    Title = td_tags[1].text
    Worldwide = td_tags[2].text
    Domestic = td_tags[3].text
    Domestic_percent = td_tags[4].text
    Foreign = td_tags[5].text
    Foreign_percent = td_tags[6].text
    return Title, Worldwide, Domestic, Domestic_percent, Foreign, Foreign_percent
def scrape_info(year_url):
    box_doc = get_box_office_page(year_url)
    box_office = box_doc.find_all('tr')[1:26]  # Adjust the slicing as needed

    for tr in box_office:
        info = get_box_office_info(tr)
        title, worldwide, domestic, domestic_percent, foreign_, foreign_percent = info
        # Check if the title already exists in the Movies table
        cursor.execute("SELECT movie_id FROM Movies WHERE title = ?", (title,))
        result = cursor.fetchone()

        if result is None:
            # Insert new movie record
            cursor.execute("INSERT INTO Movies (title) VALUES (?)", (title,))
            movie_id = cursor.lastrowid
        else:
            movie_id = result[0]

        # Insert into BoxOffice table
        cursor.execute('''INSERT INTO BoxOffice (movie_id, worldwide, domestic, 
                        domestic_percent, "foreign_", foreign_percent) 
                        VALUES (?, ?, ?, ?, ?, ?)''', 
                        (movie_id, worldwide, domestic, domestic_percent, foreign_, foreign_percent))

    conn.commit()

year_url = 'https://www.boxofficemojo.com/year/world/2022/'  # Example URL
scrape_info(year_url)
