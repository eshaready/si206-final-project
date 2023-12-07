import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('bell.db')
cursor = conn.cursor()

# Query the data from the 'Joined' table
query = "SELECT Movie_Gross, Average_Precip FROM Joined;"
cursor.execute(query)
data = cursor.fetchall()

conn.close()

# Extracting columns for plotting
movie_gross = [row[0] for row in data]
average_precip = [row[1] for row in data]

# Plotting the scatter plot
coefficients = np.polyfit(movie_gross, average_precip, 1)
line_of_best_fit = np.polyval(coefficients, movie_gross)
plt.scatter(movie_gross, average_precip)
plt.plot(movie_gross, line_of_best_fit)
plt.title('Correlation between Movie Gross and Average Precipitation')
plt.xlabel('Movie Gross')
plt.ylabel('Average Precipitation')
plt.show()