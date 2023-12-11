import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import group_part
data = group_part.data

movie_gross = []
average_precip = []
for year in data:
    for month in year:
        movie_gross.append(month["box office gross"]/10**9)
        average_precip.append(month["monthly precip avg"])

import group_part
data = group_part.data

movie_gross = []
average_precip = []
for year in data:
    for month in year:
        movie_gross.append(month["box office gross"]/10**9)
        average_precip.append(month["monthly precip avg"])


# Plotting the scatter plot
coefficients = np.polyfit(movie_gross, average_precip, 1)
line_of_best_fit = np.polyval(coefficients, movie_gross)
plt.scatter(movie_gross, average_precip)
# plt.plot(movie_gross, a*movie_gross+b)
plt.plot(movie_gross, line_of_best_fit)
plt.title('Correlation between Movie Gross and Average Precipitation')
plt.xlabel('Movie Gross (billions of dollars)')
plt.ylabel('Average Precipitation (mm)')
plt.show()