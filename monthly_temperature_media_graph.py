import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
import group_part
data = group_part.data

year = 2016  # Change me!
year_index = group_part.years.index(year)

book_titles = []
movie_titles = []
for month in data[year_index]:
    book_titles.append(month["book title"])
    movie_titles.append(month["box office title"])
book_and_movie_titles = []
for i in range(0, len(book_titles)):
    book_and_movie_titles.append(f"Book: {book_titles[i]}\nMovie: {movie_titles[i]}")

dataframe_data = []
for month in data[year_index]:
    dataframe_data.append((month["year"], month["month"], month["monthly temp avg"], month["book title"], month["box office title"]))

df = pd.DataFrame(dataframe_data, columns = ["year", "month", "monthly temp avg", "book title", "box office title"])
fig, ax = plt.subplots()
p = sns.barplot(y="month", x="monthly temp avg", orient="h", data=df)
ax.bar_label(p.containers[0], labels=book_and_movie_titles, padding = 100, label_type="center", fontsize = 8)
plt.title(f'Temperature by Month in {year} and Most Popular Book/Movie per Month')
plt.xlabel('Average Temperature (C)')
plt.ylabel('Month')
plt.xlim([-5, 40])
plt.show()