import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor


def download_images(all_books_url: str, num_pages: int):
    image_directory = "images"

    with ThreadPoolExecutor() as executor:
        for num_page in range(1, num_pages + 1):
            page_url = (
                urljoin(all_books_url, f"index.html")
                if num_page == 1
                else urljoin(all_books_url, f"catalogue/page-{num_page}.html")
            )
            print(page_url, "download images")
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, "html.parser")

            books_links = soup.find_all("h3")

            for book_link in books_links:
                book_url = urljoin(page_url, book_link.a["href"])
                book_response = requests.get(book_url)
                book_soup = BeautifulSoup(book_response.content, "html.parser")
                image_element = book_soup.find("img", {"class": "thumbnail"})
                image_url = image_element.get("src") if image_element else ""

                if image_url:
                    image_name = image_element.parent["href"].split("/")[-2]
                    image_filename = f"{image_name}.jpg"
                    image_path = os.path.join(image_directory, image_filename)

                    # Enregistrer l'image
                    executor.submit(save_image_from_url, image_url, image_path)


def save_image_from_url(image_url: str, destination_path: str):
    base_url = "https://books.toscrape.com/"
    final_url = urljoin(base_url, image_url)
    response = requests.get(final_url)
    response.raise_for_status()

    with open(destination_path, "wb") as file:
        file.write(response.content)
