from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_soup(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text,"html.parser")
  return soup

def get_data(ticker:str,period = 24):
    url = f'https://stockanalysis.com/stocks/{ticker.lower()}/history/'
    soup = get_soup(url)
    rows = soup.find_all('tr', class_="svelte-2d4szo")

    date_format = "%b %d, %Y"
    extracted_data = []
    for row in rows[:period]:   
        # Extract all <td> values from each row
        cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
        if cells:  # Ensure row has valid data
            extracted_data.append(cells)

    result_dict = []
    for i in range(0, len(extracted_data)):
        temp_dict = {
            "timestamp": int(datetime.strptime(extracted_data[i][0],date_format).timestamp()),
            "price": float(extracted_data[i][5]),
            "Volume": int((extracted_data[i][7]).replace(",", "")),
        }
        result_dict.append(temp_dict)
    return result_dict