import csv
import requests
import time
from bs4 import BeautifulSoup
from extract_data_page import get_book_data
from urllib.parse import urljoin
from download_img import download_images
from concurrent.futures import ThreadPoolExecutor


def get_num_pages(all_books_url):
    response = requests.get(all_books_url)
    soup = BeautifulSoup(response.content, "html.parser")
    num_pages = int(soup.find("li", {"class": "current"}).text.strip().split()[-1])
    return num_pages


def extract_books(all_books_url, num_pages):
    book_list = []

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

    return book_list


def add_books_in_csv(filename, fieldnames, book_list):
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Écrit les titres de colonne
        writer.writeheader()

        # Écrit les données de chaque livre
        for book in book_list:
            if book is not None:
                writer.writerow(book)


def extract_and_download_books():
    # démarrage timer
    start_time = time.time()

    # Ouvrir la page Web de la categorie et obtenir son contenu HTML
    all_books_url = "http://books.toscrape.com"

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

    num_pages = get_num_pages(all_books_url)

    with ThreadPoolExecutor() as executor:
        # Exécution en parallèle de extract_books, add_books_in_csv et download_images
        executor.submit(download_images, all_books_url, num_pages)
        extract_books_task = executor.submit(extract_books, all_books_url, num_pages)
        book_list = extract_books_task.result()
        executor.submit(add_books_in_csv, filename, fieldnames, book_list)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'extraction :", execution_time, "secondes")


extract_and_download_books()
