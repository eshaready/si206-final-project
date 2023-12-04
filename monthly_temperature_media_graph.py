import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('bell.db')
cur = conn.cursor()

# Query data 
cur.execute(
    "SELECT Year, Month, Average_Temp, Book_Title, Movie_Title FROM Joined WHERE Year = 2020"
)
data = cur.fetchall()
conn.close()
book_titles = [row[3] for row in data]
print(book_titles)

df = pd.DataFrame(data, columns = ["Year", "Month", "Average_Temp", "Book_Title", "Movie_Title"])
fig, ax = plt.subplots()
sns.barplot(x="Average_Temp", y="Month", orient="h", data=df)
ax.bar_label(labels=book_titles)
# g = sns.FacetGrid(df, row="Year")
# g.map_dataframe(sns.barplot, x="Average_Temp", y="Month", orient="h")
# ax.bar_label()
plt.show()