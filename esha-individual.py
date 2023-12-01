import time
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
        Columns: Date (bestsellers_date), Year, Month, ISBN (primary_isbn13)
        Notes: For first week of each month, get the top book [index 0] from the fiction & nonfiction list [list 0 and 1]
        First week of each month instead of every week due to rate-limit reasons
    Table 2: from https://api.nytimes.com/svc/books/v3/reviews.json?api_key={API_KEY}&isbn={ISBN}
        Reviews.
        Columns: ISBN, Title (results[book_title]), Review_URL (results[url]), Reviewer (byline)
    Table 3: from https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date={date}&api_key={API_KEY}
        Books.
        Columns: ISBN (primary_isbn13), Title (title), Author (author), Description (description), Cover (book_image)
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "books.db")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Bestsellers (Date INTEGER, Year INTEGER, Month INTEGER, ISBN INTEGER, PRIMARY KEY(Date, ISBN))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Reviews (ISBN INTEGER, Title TEXT, Review_URL TEXT UNIQUE, Reviewer TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Books (ISBN INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Description TEXT, Cover TEXT)"
    )

    return conn, cur


def insert_bestsellers_data(year, conn, cur):
    """
    Collect data for the given year (2012-present), for 12 pieces of data per database total and insert into the Bestsellers table.
    """
    # Collect data for the Bestsellers table
    # From https://api.nytimes.com/svc/books/v3/lists/overview.json?published_date={date}&api_key={API_KEY}
    # Date in format YYYY-MM-DD
    # The API goes to the closest in the future bestsellers list 
    # Year has to be 2012 or later because that's when Combined Print & E-Book Fiction is an option lol

    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    
    # Adding full, formatted dates to query to list
    dates = []
    for month in months:
        dates.append(f"{year}-{month}-01")
    
    # Send requests to the API 
    for date in dates:
        params = {"published_date": date, "api-key": API_KEY}
        r = requests.get("https://api.nytimes.com/svc/books/v3/lists/overview.json", params = params)
        data = r.content
        data = json.loads(data)
        data = data["results"]
        # Now insert that data into the table
        cur.execute(
            "INSERT OR IGNORE INTO Bestsellers (Date, Year, Month, ISBN) VALUES (?,?,?,?)",
            (data["bestsellers_date"], data["bestsellers_date"][0:4], data["bestsellers_date"][5:7], data["lists"][0]["books"][0]["primary_isbn13"], )
        )
        print("Finished adding a row! Now cooling down between requests...", data["bestsellers_date"], data["bestsellers_date"][0:4],
               data["bestsellers_date"][5:7], data["lists"][0]["books"][0]["primary_isbn13"])
        time.sleep(12)

    conn.commit()


def insert_books_data(conn, cur):
    """Will insert detailed data for 25 of the books in the bestsellers list."""
    count = 0
    books = cur.execute(
        "SELECT Date, ISBN FROM Bestsellers", multi = True
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
        params = {"published_date": date, "api-key": API_KEY}
        r = requests.get("https://api.nytimes.com/svc/books/v3/lists/overview.json", params = params)
        data = r.content
        data = json.loads(data)
        data = data["results"]
        cur_book = data["lists"][0]["books"][0]

        # Known that this is the book that got added to Bestsellers. But sanity check! 
        if cur_book["primary_isbn13"] != isbn:
            print("Error!! The book being added to books isn't correct!")
            break

        # Now finally, add more info about it to Books
        cur.execute(
            "INSERT OR IGNORE INTO Books (ISBN, Title, Author, Description, Cover) VALUES (?,?,?,?,?)",
            (cur_book["primary_isbn13"], cur_book["title"], cur_book["author"], cur_book["description"], cur_book["book_image"], )
        )
        conn.commit()

        if count >= 25:
            break
        print("Finished adding a row! Now cooling down between requests...", count, isbn)
        time.sleep(12)


def insert_reviews_data(conn, cur):
    """Will insert reviews data for 25 of the books in the bestsellers list."""
    count = 0
    books = cur.execute(
        "SELECT ISBN FROM Bestsellers", multi = True
    )
    for row in books:
        isbn = row[0]

        # Now check if the book data is already present in Books 
        cur.execute(
            "SELECT * FROM Reviews WHERE ISBN = ?", (isbn,)
        )

        should_break = False
        for row in cur:
            # If it goes in here then the data was already in books! So restart the loop w the next book
            should_break = True
        if should_break:
            continue

        # By here, the current book data wasn't already present. So add it
        params = {"isbn": isbn, "api-key": API_KEY}
        r = requests.get("https://api.nytimes.com/svc/books/v3/reviews.json", params = params)
        data = r.content
        data = json.loads(data)
        if data.get("fault", None) is not None:
            print("API quota reached :()")
            continue
        data = data["results"]
        for result in data:
            count += 1  # count needs to be here bc multiple reviews can be added per book
            cur.execute(
                "INSERT OR IGNORE INTO Reviews (ISBN, Title, Review_URL, Reviewer) VALUES (?,?,?)",
                (isbn, result["book_title"], result["url"], result["byline"],)
            )
        conn.commit()
        
        if count >= 25:
            break
        print("Finished adding a row! Now cooling down between requests...", count, isbn)
        time.sleep(12)


# ! MAIN 
conn, cur = create_database()
user_input = input("Do you want to add to the Bestsellers database by year [0], populate the Books database [1], or populate the Reviews database [2]? (q for quit) ")
while user_input != "q":
    if user_input == "0":
        # Add to the Bestsellers database by year 
        year = input("Enter a year between 2012-present (inclusive) (format YYYY) to gather data from: ")
        insert_bestsellers_data(year, conn, cur)
        print(f"Added data to the Bestsellers database for {year}!...\n")
    elif user_input == "1":
        # Populate the Books database 
        insert_books_data(conn, cur)
        print("Populated 25 books in the Books database!...\n")
    elif user_input == "2":
        # Populate the Reviews database 
        insert_reviews_data(conn, cur)
        print("Populated 25 reviews in the Reviews database!...\n")
    user_input = input("Do you want to add to the Bestsellers database by year [0], populate the Books database [1], or populate the Reviews database [2]? (q for quit) ")