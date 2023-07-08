import requests
import csv
from bs4 import BeautifulSoup
import re
import time

URL = "https://quotes.toscrape.com"
VALID_PATTERN = r"^[a-z][a-z-]*[a-z]$"

user_tag = input("Enter a tag which:\n"
                 "\t1.only consists of lowercase english letters and '-'\n"
                 "\t2.starts and ends with letters: ")

if re.match(VALID_PATTERN, user_tag):

    page = requests.get(f"{URL}/tag/{user_tag}")
    soup = BeautifulSoup(page.content, "html.parser")

    if f"{soup.findAll('div', class_='col-md-8')[1].text.strip()}" != "No quotes found!":

        quotes = list(soup.findAll("span", class_="text"))
        authors = list(soup.findAll("small", class_="author"))

        next_button = soup.find("li", class_="next")
        if next_button is not None:
            time.sleep(40)
            page_2 = requests.get(f"{URL}{next_button.find('a').get('href')}")
            soup_2 = BeautifulSoup(page_2.content, "html.parser")
            quotes.extend(list(soup_2.findAll("span", class_="text")))
            authors.extend(list(soup_2.findAll("small", class_="author")))

        csv_file = open(f"{user_tag}_quotes.csv", "w", encoding="UTF-8", newline='')
        writer = csv.writer(csv_file)
        for quote, author in zip(quotes, authors):
            writer.writerow([quote.text.strip()])
            writer.writerow([author.text.strip()])
        csv_file.close()
        print("CSV file successfully created")

    else:
        print(f"No quotes were found for the tag: {user_tag}")
else:
    print("Invalid tag.")
