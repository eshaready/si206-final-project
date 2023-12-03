import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "bell.db")
cur = conn.cursor()

def attach_databases():
    books_path = path + "/" + "books.db"
    cur.execute(
        "ATTACH ? AS 'books'", (books_path)
    )
    boxoffice_path = path + "/" + "box_office.db"
    cur.execute(
        "ATTACH ? AS 'box_office'", (boxoffice_path)
    )
    # Weather data is already in there as its own table
    conn.commit()

def join_data(year):
    """To select all the data joined for one year."""
    cur.execute(
        "SELECT * FROM books.Bestsellers JOIN books.Books ON books.Bestsellers.ISBN = books.Books.ISBN "
        "JOIN box_office.[TABLENAME] ON books.Bestsellers.Year = box_office.[TABLENAME].year "
        "AND books.Bestsellers.Month = box_office.[TABLENAME].month "
        "JOIN monthly_averages ON books.Bestsellers.Year = monthly_averages.year "
        "AND books.Bestsellers.Month = monthly_averages.month WHERE year = ?", (year)
    )
    # Need to calculate something based on 