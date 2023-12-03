import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "bell.db")
cur = conn.cursor()

def attach_databases():
    # books_path = path + "/" + "books.db"
    cur.execute(
        "ATTACH DATABASE 'books.db' AS books"
    )
    # boxoffice_path = path + "/" + "box_office.db"
    cur.execute(
        "ATTACH DATABASE 'box_office.db' AS box_office"
    )
    # Weather data is already in there as its own table
    conn.commit()

def join_data(year):
    """To select all the data joined for one year."""
    cur.execute('''
        SELECT books.Bestsellers.Year, books.Bestsellers.Month, books.Books.Title, books.Books.Author, books.Books.Description,
        books.Books.Cover, box_office.TopMonthlyReleases.title, box_office.TopMonthlyReleases.gross, monthly_averages.tempmax,
        monthly_averages.tempmin, monthly_averages.temp, monthly_averages.precip
        FROM books.Bestsellers JOIN books.Books ON books.Bestsellers.ISBN = books.Books.ISBN 
        JOIN box_office.TopMonthlyReleases ON books.Bestsellers.Year = box_office.TopMonthlyReleases.year 
        AND books.Bestsellers.Month = box_office.TopMonthlyReleases.month 
        JOIN monthly_averages ON books.Bestsellers.Year = monthly_averages.year 
        AND books.Bestsellers.Month = monthly_averages.month WHERE books.Bestsellers.year = ?
    ''', (year,))
    # Need to calculate something based on this; for now just printing
    for row in cur:
        print(row)


# ! MAIN 
attach_databases()
join_data(2012)