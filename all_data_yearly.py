import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read data from averaged_by_year.csv
df = pd.read_csv('averaged_by_year.csv')

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Plot tempmax, tempmin, temp, and precipitation by year
sns.lineplot(x='year', y='tempmax', data=df, label='Temp Max', marker='o')
sns.lineplot(x='year', y='tempmin', data=df, label='Temp Min', marker='o')
sns.lineplot(x='year', y='temp', data=df, label='Temp', marker='o')
sns.lineplot(x='year', y='precip', data=df, label='Precipitation', marker='o')

# Set plot labels and title
plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Temperature and Precipitation Trends by Year')

# Display legend
plt.legend()

# Show the plot
plt.show()
