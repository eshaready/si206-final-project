import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('bell.db')
cursor = conn.cursor()

# Query the data from the 'Joined' table
query = "SELECT Movie_Gross, Average_Temp, Month FROM Joined;"
cursor.execute(query)
data = cursor.fetchall()

conn.close()

# Extracting columns for plotting
movie_gross = [row[0] for row in data]
average_temp = [row[1] for row in data]
month = [str(row[2]) for row in data]

# Plotting the scatter plot
sns.scatterplot(x=movie_gross, y=average_temp, hue=month)
plt.title('Correlation between Movie Gross and Average Temperature')
plt.xlabel('Movie Gross')
plt.ylabel('Average Temperature')
plt.legend(labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
plt.show()