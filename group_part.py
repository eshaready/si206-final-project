import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + "bell.db")
cur = conn.cursor()

def join_databases():
    books_path = path + "/" + "books.db"
    cur.execute(
        "ATTACH ? AS 'books'", (books_path)
    )

    weather_path = path + "/" + ".db"
    boxoffice_path = path + "/" + ".db"