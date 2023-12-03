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

    data = []
    # 0 year, 1 month, 2 book title, 3 book author, 4 book description, 5 book cover, 6 box office title, 7 box office gross, 
    # 8 monthly max temp avg, 9 monthly min temp avg, 10 monthly temp avg, 11 monthly precipitation avg
    for row in cur:
        data.append({"year": row[0], "month": row[1], "book title": row[2], "book author": row[3], "book desc": row[4], 
                    "book cover": row[5], "box office title": row[6], "box office gross": row[7], "monthly max temp avg": row[8], 
                    "monthly min temp avg": row[9], "monthly temp avg": row[10], "monthly precip avg": row[11]})
    return data

def calculate_data(data):
    """
    Calculations: 
    1: Month | Average gross per month | Min ISBN that month | Max ISBN that month | Monthly temperature average | Monthly precipitation average
    2: Year | Average gross per year | Min ISBN that year | Max ISBN that year | Average ISBN that year | Yearly temp average 
    """
    # 1
    monthly_data = {}
    for _ in range(0, 12)
    with open("joined_data_monthly_calculations.csv", "w", newline='') as f:
        headers = ["Month", "Avg gross", "Min ISBN", "Max ISBN", "Temp avg", "Precip avg"]



# ! MAIN 
attach_databases()

years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
data = []
for year in years:
    data.append(join_data(year))