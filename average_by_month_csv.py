import csv
from collections import defaultdict
from datetime import datetime

# creates an average_by_month csv file
def average_by_month():
    # Initialize dictionaries to store monthly data with each month having the following dict as default value
    monthly_data = defaultdict(lambda: {'tempmax': [], 'tempmin': [], 'temp': [], 'precip': []})

    # Read data from each CSV file
    for year in range(2012, 2023):
        filename = f"{year}.csv"
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date = datetime.strptime(row['datetime'], '%Y-%m-%d')
                month_key = f"{date.year}{date.month:02d}"
                monthly_data[month_key]['tempmax'].append(float(row['tempmax']))
                monthly_data[month_key]['tempmin'].append(float(row['tempmin']))
                monthly_data[month_key]['temp'].append((float(row['tempmax']) + float(row['tempmin'])) / 2)
                monthly_data[month_key]['precip'].append(float(row['precip']))

    # Calculate the monthly averages
    averaged_data = []
    for month, values in sorted(monthly_data.items()):
        avg_tempmax = sum(values['tempmax']) / len(values['tempmax'])
        avg_tempmin = sum(values['tempmin']) / len(values['tempmin'])
        avg_temp = sum(values['temp']) / len(values['temp'])
        avg_precip = sum(values['precip']) / len(values['precip'])
        year = int(month[:4])
        month_num = int(month[4:])
        averaged_data.append({'date': f"{year}{month_num:02d}", 'year': year, 'month': month_num, 'tempmax': avg_tempmax, 'tempmin': avg_tempmin, 'temp': avg_temp, 'precip': avg_precip})

    # Write the results to a new CSV file
    with open('averaged_by_month.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'year', 'month', 'tempmax', 'tempmin', 'temp', 'precip']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in averaged_data:
            writer.writerow(row)

average_by_month()