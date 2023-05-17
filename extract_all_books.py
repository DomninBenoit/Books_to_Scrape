import csv
import requests
import time
from bs4 import BeautifulSoup
from extract_data_page import get_book_data
from urllib.parse import urljoin
from download_img import download_images

# démarrage timer
start_time = time.time()

# Ouvrir la page Web de la categorie et obtenir son contenu HTML
all_books_url = "http://books.toscrape.com"

response = requests.get(all_books_url)
soup = BeautifulSoup(response.content, "html.parser")
num_pages = int(soup.find("li", {"class": "current"}).text.strip().split()[-1])
book_list = []

# Écrit les données dans un fichier CSV
filename = "all_books_data.csv"
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

# Liste des liens des livres
for num_page in range(1, num_pages + 1):
    page_url = (
        urljoin(all_books_url, f"index.html")
        if num_page == 1
        else urljoin(all_books_url, f"catalogue/page-{num_page}.html")
    )
    print(page_url)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    books_links = soup.find_all("h3")

    # Ajout livre par livre
    for book_link in books_links:
        book_url = urljoin(page_url, book_link.find("a")["href"])
        book_list.append(get_book_data(book_url))


with open(filename, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Écrit les titres de colonne
    writer.writeheader()

    # Écrit les données de chaque livre
    for book in book_list:
        if book is not None:
            writer.writerow(book)

    download_images(filename, fieldnames)

end_time = time.time()
execution_time = end_time - start_time
print("Temps d'extraction :", execution_time, "secondes")
