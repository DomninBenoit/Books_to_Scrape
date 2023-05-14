import csv
import requests
from bs4 import BeautifulSoup
from extract_data_page import get_book_data
from urllib.parse import urljoin

# Ouvrir la page Web de la categorie et obtenir son contenu HTML
category_url = (
    "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
)
response = requests.get(category_url)
soup = BeautifulSoup(response.content, "html.parser")
num_pages = int(soup.find("li", {"class": "current"}).text.strip().split()[-1])


# Liste des liens des livres
book_list = []
books_links = soup.find_all("h3")

# Ajout livre par livre
for book_link in books_links:
    book_url = urljoin(category_url, book_link.find("a")["href"])
    book_list.append(get_book_data(book_url))

# Écrit les données dans un fichier CSV
fieldnames = [
    "product_page_url",
    "upc",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
]
filename = "category_data.csv"
with open(filename, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Écrit les titres de colonne
    writer.writeheader()

    # Écrit les données de chaque livre
    for book in book_list:
        writer.writerow(book)
