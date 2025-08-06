import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://www.scrapethissite.com/pages/forms/'
page_num = 1
result = []

while True:
    # url for pagination
    url = f"{BASE_URL}?page_num={page_num}&per_page=100"
    print(f"fetching page {url}")

    # check page number valid or not
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table")
    rows = soup.findAll("tr", class_="team")

    # check row have data or not 
    if not rows:
        print(f"No more data on page {page_num}")
        break

    # get data
    for row in rows:
        team_name = row.find("td", class_="name").get_text(strip=True)
        year = row.find("td", class_="year").get_text(strip=True)
        pct = row.find("td", class_="pct").get_text(strip=True) # Win %

        result.append({
            "team_name": team_name,
            "year": year,
            "pct": pct
        })

    # next pagination
    page_num += 1

# Save to CSV
with open("teams_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["team_name", "year", "pct"])
    writer.writeheader()
    writer.writerows(result)

print("Data saved to teams_data.csv")