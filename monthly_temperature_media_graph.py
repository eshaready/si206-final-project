import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('bell.db')
cur = conn.cursor()

year = 2013

# Query data 
cur.execute(
    "SELECT Year, Month, Average_Temp, Book_Title, Movie_Title FROM Joined WHERE Year = ?", (year,)
)
data = cur.fetchall()
conn.close()
book_titles = [row[3] for row in data]
print(book_titles)

df = pd.DataFrame(data, columns = ["Year", "Month", "Average_Temp", "Book_Title", "Movie_Title"])
fig, ax = plt.subplots()
p = sns.barplot(x="Average_Temp", y="Month", orient="h", data=df)
ax.bar_label(p.containers[0], labels=book_titles)
plt.title(f'Temperature by Month in {year} and Bestselling Book per Month')
plt.xlabel('Average Temperature')
plt.ylabel('Month')
plt.show()