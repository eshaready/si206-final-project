import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('averaged_by_month.csv')

# Pivot the DataFrame to create a matrix for the heatmap
heatmap_data = df.pivot(index='month', columns='temp', values='tempmax')

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Create the heatmap using seaborn
sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".1f", linewidths=0.5) # show to 1 decimal place

# Set plot labels and title
plt.xlabel('Average Temperature')
plt.ylabel('Month')
plt.title('Heatmap of Average Monthly Temperature')

plt.show()