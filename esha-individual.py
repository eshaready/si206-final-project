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
        Columns: Date (bestsellers_date), ISBN (primary_isbn10)
        Notes: For each week, get the top book [index 0] from the fiction & nonfiction list [list 0 and 1]
    Table 2: from https://api.nytimes.com/svc/books/v3/reviews.json?api_key={API_KEY}&isbn={ISBN}
        Reviews.
        Columns: ISBN, Title (results[book_title]), Review_URL (from results[url])
    Table 3: from https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date={date}&api_key={API_KEY}
        Books.
        Columns: ISBN (primary_isbn10), Title (title), Author (author), Description (description), Cover (book_image)
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "books.db")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Bestsellers (Date INTEGER, ISBN INTEGER, PRIMARY KEY(Date, ISBN))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Reviews (ISBN INTEGER, Title TEXT, Review_URL TEXT UNIQUE)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Books (ISBN INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Description TEXT, Cover TEXT)"
    )

    return conn, cur

# Function to collect best-selling list and also reviews for those books for an inputted year
def insert_bestsellers_data(year, half, conn, cur):
    """
    Collect data for the given year (2012-present) (from the first six months [0] or the last six months [1], 
    for 24 pieces of data per database total) and insert into the Bestsellers table.
    """
    # Collect data for the Bestsellers table
    # From https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date={date}&api_key={API_KEY}
    # Date in format YYYY-MM-DD
    # The API goes to the closest in the future bestsellers list 
    # Year has to be 2012 or later because that's when Combined Print & E-Book Fiction is an option lol

    # Getting months to query
    if half == 0:
        # First half of the year
        months = ["01","02","03","04","05","06"]
    else:
        # Second half of the year
        months = ["07","08","09","10","11","12"]

    # Getting days to query 
    days = ["01","07","14","21"]
    
    # Adding full, formatted dates to query to list
    dates = []
    for month in months:
        for day in days:
            date = f"{year}-{month}-{day}"
            dates.append(date)
    
    # Send requests to the API 
    for date in dates:
        params = {"published_date": date, "api_key": API_KEY}
        r = requests.get("https://api.nytimes.com/svc/books/v3/lists/overview.json", params = params)
        data = r.content
        data = data["results"]
        # Now insert that data into the table
        cur.execute(
            "INSERT OR IGNORE INTO Bestsellers (Date, ISBN) VALUES (?,?)",
            (data["bestsellers_date"], data["lists"][0]["books"][0]["primary_isbn10"], )
        )

    conn.commit()

def insert_books_data(conn, cur):
    """Will insert detailed data for 25 of the books in the bestsellers list."""
    count = 0
    books = cur.execute(
        "SELECT Date, ISBN FROM Bestsellers",  multi = True
    )
    for row in books:
        date = row[0]
        isbn = row[1]
        # Now check if the book data is already present in Books 
        cur.execute(
            "SELECT * FROM Books WHERE ISBN = ?", (isbn,)
        )

        should_break = False
        for row in cur:
            # If it goes in here then the data was already in books! So restart the loop w the next book
            should_break = True
        if should_break:
            continue

        # By here, the current book data wasn't already present. So add it
        count += 1
        params = {"published_date": date, "api_key": API_KEY}
        r = requests.get("https://api.nytimes.com/svc/books/v3/lists/overview.json", params = params)
        data = r.content
        data = data["results"]
        cur_book = data["lists"][0]["books"][0]

        # Known that this is the book that got added to Bestsellers. But sanity check! 
        if cur_book["primary_isbn10"] != isbn:
            print("Error!! The book being added to books isn't correct!")
            break

        # Now finally, add more info about it to Books
        cur.execute(
            "INSERT OR IGNORE INTO Books (ISBN, Title, Author, Description, Cover) VALUES (?,?,?,?,?)",
            (cur_book["primary_isbn10"], cur_book["title"], cur_book["author"], cur_book["description"], cur_book["book_image"], )
        )
        conn.commit()

        if count >= 25:
            break




def insert_reviews_data(conn, cur):
    """Will insert reviews data for 25 of the books in the bestsellers list."""
    pass
    
    