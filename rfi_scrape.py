import requests
import csv
from datetime import datetime, timedelta

def scrape_and_save_rainfall_data():
    base_url = 'http://121.58.193.173:8080/rainfall/map_list.do?ymdhm='
    obsnm_list = ["Nangka", "Mt. Oro", "San Mateo-2", "Marikina (Youth Camp)"]
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 10, 12)
    current_date = start_date

    with open('rainfall_data.csv', 'w', newline='') as csvfile:
        fieldnames = ["station", "year", "month", "day", "hour", "rainfall"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write CSV header
        writer.writeheader()

        while current_date <= end_date:
            formatted_date = current_date.strftime('%Y%m%d%H%M')
            url = f"{base_url}{formatted_date}"

            try:
                response = requests.get(url)
                data = response.json()

                for entry in data:
                    if entry['obsnm'] in obsnm_list:
                        year = int(formatted_date[:4])
                        month = datetime.strptime(formatted_date[4:6], '%m').strftime('%B')
                        day = int(formatted_date[6:8])
                        hour = int(formatted_date[8:10])
                        rainfall = entry.get('rf', 'null')
                        
                        writer.writerow({
                            'station': entry['obsnm'],
                            'year': year,
                            'month': month,
                            'day': day,
                            'hour': hour,
                            'rainfall': rainfall
                        })

            except Exception as e:
                print(f"Error fetching data for {formatted_date}: {e}")

            # Increment to the next hour
            current_date += timedelta(hours=1)

if __name__ == "__main__":
    scrape_and_save_rainfall_data()
