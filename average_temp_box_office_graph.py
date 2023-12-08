import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import group_part
data = group_part.data

# Extracting columns for plotting
movie_gross = []
average_temp = []
month = []
for year in data:
    for m in year:
        movie_gross.append(m["box office gross"]/10**9)
        average_temp.append(m["monthly temp avg"])
        month.append(str(m["month"]))
        

# Plotting the scatter plot
sns.lineplot(x=movie_gross, y=average_temp, hue=month)
sns.scatterplot(x=movie_gross, y=average_temp, hue=month)
plt.title('Correlation between Movie Gross and Average Temperature by Month')
plt.xlabel('Movie Gross (billions of dollars)')
plt.ylabel('Average Temperature (C)')
plt.legend(labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
plt.show()