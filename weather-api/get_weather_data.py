# weather data across the entire United States for each year from 2012-2022
import requests
import sys
import csv

def get_weather_data(year):
    # I get rate limited for how many days of data I can request per day, 
    # and I have to get data year by year instead of 11 years all at once
    response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/United%20States/{year}-01-01/{year}-12-31?unitGroup=metric&include=days&key=2AMFZFKRG88567QNEPA2AGNHT&contentType=csv")
    if response.status_code != 200:
        print('Unexpected Status code: ', response.status_code)
        sys.exit()

    CSVText = csv.reader(response.text.splitlines(), delimiter=',',quotechar='"')
    with open(f'{year}.csv', 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)

        for row in CSVText:
            csv_writer.writerow(row)

year = input("Enter a year to gather data from (YYYY): ")
get_weather_data(year)