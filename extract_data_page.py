from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv


def get_book_data(url_link):
    # Ouvrir la page Web et obtenir son contenu HTML
    url = urljoin("http://books.toscrape.com/catalogue/", url_link)
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

    # Stocker les données dans un dictionnaire
    book = {
        "product_page_url": product_page_url,
        "upc": upc,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }

    # Vérification extraction avec succès
    if not all(book.values()):
        return None

    return book
