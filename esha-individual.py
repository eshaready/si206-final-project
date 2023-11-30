import requests
import json
import os
import sqlite3

# Access NYT books API 
API_KEY = "E6OgHNRRlwLQhlhMmK9TAi3aX9OGuDj9"

# Set up database 
def create_database():
    """
    Create the database and two tables for the NYT API portion of the project.

    Table 1: from https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date={date}&api_key={API_KEY}
        Bestsellers. 
        Columns: Date (bestsellers_date), ISBN (primary_isbn10), Title (title), Author (author), Description (description)
        Notes: For each week, get the top book [index 0] from the fiction & nonfiction list [list 0 and 1]
    Table 2: from https://api.nytimes.com/svc/books/v3/reviews.json?api_key={API_KEY}&isbn={ISBN}
        Reviews.
        Columns: ISBN, Title (results[book_title]), Review_URL (from results[url])
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "books.db")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Bestsellers (Date INTEGER, ISBN INTEGER, Title TEXT, Author TEXT, Description TEXT, PRIMARY KEY (ISBN, Date))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Reviews (ISBN INTEGER PRIMARY KEY, Title TEXT, Review_URLs TEXT)"
    )

    return conn, cur

# Function to collect best-selling list and also reviews for those books for an inputted year
def insert_bestsellers_data(year, half, conn, cur):
    """
    Collect data for the given year (from the first six months or the last six months, for 24 pieces of data per database total)
    and insert into the Bestsellers table.
    """
    # First: collect data for the Bestsellers table
    # From https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date={date}&api_key={API_KEY}
    # The API goes to the closest in the future bestsellers list 

    # Getting months to query
    if half == 0:
        # First half of the year
        months = [1,2,3,4,5,6]
    else:
        # Second half of the year
        months = [7,8,9,10,11,12]

    # Getting days to query 
    days = [1,7,14,21]
    