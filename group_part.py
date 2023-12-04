import sqlite3
import os
import csv

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "bell.db")
cur = conn.cursor()

def attach_databases():
    """
    Attach the databases/import the tables into the overall database.
    No inputs or outputs.
    """
    # books_path = path + "/" + "books.db"
    cur.execute(
        "ATTACH DATABASE 'books.db' AS books"
    )
    # boxoffice_path = path + "/" + "box_office.db"
    cur.execute(
        "ATTACH DATABASE 'box_office.db' AS box_office"
    )
    # Weather data is already in there as its own table

    # Copy tables from books.db to bell.db 
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Bestsellers (Date INTEGER, Year INTEGER, Month INTEGER, ISBN INTEGER, PRIMARY KEY(Date, ISBN))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Reviews (ISBN INTEGER, Title TEXT, Review_URL TEXT UNIQUE, Reviewer TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Books (ISBN INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Description TEXT, Cover TEXT)"
    )
    cur.execute(
        "INSERT OR IGNORE INTO Bestsellers (Date, Year, Month, ISBN) SELECT * FROM Books.Bestsellers"
    )
    cur.execute(
        "INSERT OR IGNORE INTO Books (ISBN, Title, Author, Description, Cover) SELECT * FROM Books.Books"
    )
    cur.execute(
        "INSERT OR IGNORE INTO Reviews (ISBN, Title, Review_URL, Reviewer) SELECT * FROM Books.Reviews"
    )

    # Copy table from box_office.db to bell.db 
    cur.execute('''
    CREATE TABLE IF NOT EXISTS TopMonthlyReleases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        month INTEGER,
        title TEXT,
        gross TEXT,
        UNIQUE(year, month, title)
    )
    ''')
    cur.execute('''
        INSERT OR IGNORE INTO TopMonthlyReleases (year, month, title, gross) SELECT box_office.TopMonthlyReleases.year,
        box_office.TopMonthlyReleases.month, box_office.TopMonthlyReleases.title, box_office.TopMonthlyReleases.gross 
        FROM box_office.TopMonthlyReleases
    ''')
    conn.commit()

def join_data(year):
    """
    To select all the data joined for one year.
    Input: year on which to join data.
    Output: nothing.
    """
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Joined (Year INTEGER, Month INTEGER, ISBN INTEGER, Book_Title TEXT, Book_Author TEXT,
        Book_Description TEXT, Book_Cover TEXT, Movie_Title TEXT, Movie_Gross INTEGER, Average_Max_Temp REAL, 
        Average_Min_Temp REAL, Average_Temp REAL, Average_Precip REAL, PRIMARY KEY(Year, Month))
    ''')

    cur.execute('''
        SELECT Bestsellers.Year, Bestsellers.Month, Books.ISBN, Books.Title, Books.Author, 
        Books.Description, Books.Cover, TopMonthlyReleases.title, TopMonthlyReleases.gross, 
        monthly_averages.tempmax, monthly_averages.tempmin, monthly_averages.temp, monthly_averages.precip
        FROM Bestsellers JOIN Books ON Bestsellers.ISBN = Books.ISBN 
        JOIN TopMonthlyReleases ON Bestsellers.Year = TopMonthlyReleases.year 
        AND Bestsellers.Month = TopMonthlyReleases.month 
        JOIN monthly_averages ON Bestsellers.Year = monthly_averages.year 
        AND Bestsellers.Month = monthly_averages.month WHERE Bestsellers.year = ?
    ''', (year,))

    data = []
    # year, month, book isbn, book title, book author, book description, book cover, box office title, box office gross, 
    # monthly max temp avg, monthly min temp avg, monthly temp avg, monthly precipitation avg
    for row in cur:
        data.append({"year": row[0], "month": row[1], "isbn": row[2], "book title": row[3], "book author": row[4], "book desc": row[5], 
                    "book cover": row[6], "box office title": row[7], "box office gross": int(row[8][1:].replace(",", "")), "monthly max temp avg": row[9], 
                    "monthly min temp avg": row[10], "monthly temp avg": row[11], "monthly precip avg": row[12]})
    
    for row in data:
        cur.execute('''
            INSERT OR IGNORE INTO Joined (Year, Month, ISBN, Book_Title, Book_Author, Book_Description, 
            Book_Cover, Movie_Title, Movie_Gross, Average_Max_Temp, Average_Min_Temp, Average_Temp, Average_Precip)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (row["year"], row["month"], row["isbn"], row["book title"], row["book author"], row["book desc"],
              row["book cover"], row["box office title"], row["box office gross"], row["monthly max temp avg"],
              row["monthly min temp avg"], row["monthly temp avg"], row["monthly precip avg"], ))
    conn.commit()
    return data

def calculate_data(data):
    """
    Calculations: 
    1: Month | Average gross per month | Titles | Monthly temperature average | Monthly precipitation average
    2: Year | Average gross per year | Min ISBN that year | Max ISBN that year | Yearly temp average 

    Input: data for all years and all months.
    Output: Writes above calculations to csv files.
    """
    # 1
    monthly_data = []
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for i in range(0, len(months)):
        # Calculate average gross per month
        gross_sum = 0
        for year in data:
            gross_sum += year[i]["box office gross"]

        # Gather ISBNs
        titles = []
        for year in data:
            titles.append(year[i]["book title"])
        
        # Calculate average temperature per month 
        temp_sum = 0
        for year in data:
            temp_sum += year[i]["monthly temp avg"]
        
        # Calculate average precipitation per month
        precip_sum = 0
        for year in data:
            precip_sum += year[i]["monthly temp avg"]
        
        monthly_data.append({"Month": months[i],
                             "Avg gross": gross_sum / len(data),
                             "Book titles": titles,
                             "Temp avg": temp_sum / len(data),
                             "Precip avg": precip_sum / len(data)})

    with open("joined_data_monthly_calculations.csv", "w", newline='') as f:
        headers = ["Month", "Avg gross", "Book titles", "Temp avg", "Precip avg"]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in monthly_data:
            writer.writerow(row)
    
    # 2
    yearly_data = []
    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    for y in range(0, len(years)):
        # Calculate avg gross per year
        gross_sum = 0
        for m in range(0, 12):
            # looping through months in data[i]
            gross_sum += data[y][m]["box office gross"]

        # Calculate min isbn that year 
        # Calculate max isbn that year 
        min_isbn = data[y][0]["isbn"]
        max_isbn = data[y][0]["isbn"]
        for m in range(1, 12):
            if data[y][m]["isbn"] < min_isbn:
                min_isbn = data[y][m]["isbn"]
            if data[y][m]["isbn"] > max_isbn:
                max_isbn = data[y][m]["isbn"]

        # Calculate yearly temp avg 
        temp_sum = 0
        for m in range(0, 12):
            temp_sum += data[y][m]["monthly temp avg"]
        
        yearly_data.append({"Year": years[y],
                            "Avg gross": gross_sum / 12,
                            "Min ISBN": min_isbn,
                            "Max ISBN": max_isbn,
                            "Avg temp": temp_sum / 12})

    with open("joined_data_yearly_calculations.csv", "w", newline='') as f:
        headers = ["Year", "Avg gross", "Min ISBN", "Max ISBN", "Avg temp"]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in yearly_data:
            writer.writerow(row)


# ! MAIN 
attach_databases()

years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
data = []
for year in years:
    data.append(join_data(year))
calculate_data(data)