import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('averaged_by_year.csv')

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Create a bar graph for precipitation by year
plt.bar(df['year'], df['precip'], color='blue', alpha=0.7) # alpha is transparency level, 1 opaque, 0 transparent

# Set plot labels and title
plt.xlabel('Year')
plt.ylabel('Average Precipitation')
plt.title('Average Precipitation by Year')

plt.show()