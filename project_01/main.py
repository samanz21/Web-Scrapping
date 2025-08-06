import requests
from bs4 import BeautifulSoup
import csv

response = requests.get("https://www.scrapethissite.com/pages/simple/")
soup = BeautifulSoup(response.text, "html.parser")

# print(response.status_code) 
# print(response.text) # html that we see in inspect


country_block = soup.find_all("div", class_="col-md-4 country") # get from block 
# print(f"Number of countries found: {len(country_block)}")

result = []

for block in country_block:
    country_element = block.find("h3", class_="country-name")
    country_name = country_element.get_text(strip=True)

    capital_element = block.find("span", class_="country-capital")
    capital_name = capital_element.get_text(strip=True)

    population_element = block.find("span", class_="country-population")
    population_name = population_element.get_text(strip=True)

    result.append({"name": country_name, "capital": capital_name, "population" : population_name})

## print list of country and its details
# for i, item in enumerate(result, start=1): 
#     print(f"{i}. Country: {item['name']} - Capital: {item['capital']} - Population: {item['population']}")


# save into csv file
with open("countries.csv", "w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["No.", "Country", "Capital", "Population"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i, item in enumerate(result, start=1):
        writer.writerow({
            "No.": i,
            "Country": item["name"],
            "Capital": item["capital"],
            "Population": item["population"]
        })

print("✅ Data saved to countries.csv")