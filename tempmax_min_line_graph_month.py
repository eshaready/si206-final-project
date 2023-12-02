import pandas as pd
import matplotlib.pyplot as plt

monthly_average_df = pd.read_csv('averaged_by_month.csv')

# Plotting using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(monthly_average_df['month'], monthly_average_df['tempmax'], label='Average TempMax', marker='o')
plt.plot(monthly_average_df['month'], monthly_average_df['tempmin'], label='Average TempMin', marker='o')

# Customize the plot
plt.title('Monthly Average TempMax and TempMin')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)

plt.tight_layout() # edges of figure are closer to graph, graph "seems" larger
plt.show()