import sqlite3
import matplotlib.pyplot as plt
import group_part
data = group_part.data

# Extracting columns for plotting
movie_gross = []
average_precip = []
for year in data:
    for month in year:
        movie_gross.append(month["box office gross"]/10**9)
        average_precip.append(month["monthly precip avg"])

# Plotting the scatter plot
plt.scatter(movie_gross, average_precip)
plt.title('Correlation between Movie Gross and Average Precipitation')
plt.xlabel('Movie Gross (billions of dollars)')
plt.ylabel('Average Precipitation (mm)')
plt.show()