from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

# Ouvrir la page Web et obtenir son contenu HTML
url = (
    "http://books.toscrape.com/catalogue/eragon-the-inheritance-cycle-1_153/index.html"
)
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

# Extraire les informations requises
product_page_url = url
upc = soup.find("th", text="UPC").find_next_sibling("td").text
title = soup.find("h1").text
price_including_tax = (
    soup.find("th", text="Price (incl. tax)").find_next_sibling("td").text
)
price_excluding_tax = (
    soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text
)
number_available = soup.find("th", text="Availability").find_next_sibling("td").text
product_description = (
    soup.find("div", {"id": "product_description"}).find_next_sibling("p").text
)
category = soup.find(
    "a", href=lambda href: href and "category/books/" in href
).text.strip()
review_rating = soup.find("p", {"class": "star-rating"}).get("class")[1]
image_url = soup.find("img", {"class": "thumbnail"}).get("src")

# Stocker les données dans un fichier CSV
filename = "book_data.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
        ]
    )
    writer.writerow(
        [
            product_page_url,
            upc,
            title,
            price_including_tax,
            price_excluding_tax,
            number_available,
            product_description,
            category,
            review_rating,
            image_url,
        ]
    )
