from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_book_data(url_link: str) -> dict:
    # Ouvrir la page Web et obtenir son contenu HTML
    url = urljoin("http://books.toscrape.com/catalogue/", url_link)
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # Extraire les informations requises
    product_page_url = url

    upc_element = soup.find("th", text="UPC")
    upc = upc_element.find_next_sibling("td").text.strip() if upc_element else ""

    title_element = soup.find("h1")
    title = title_element.text.strip() if title_element else ""

    price_including_tax_element = soup.find("th", text="Price (incl. tax)")
    price_including_tax = (
        price_including_tax_element.find_next_sibling("td").text.strip()
        if price_including_tax_element
        else ""
    )

    price_excluding_tax_element = soup.find("th", text="Price (excl. tax)")
    price_excluding_tax = (
        price_excluding_tax_element.find_next_sibling("td").text.strip()
        if price_excluding_tax_element
        else ""
    )

    number_available_element = soup.find("th", text="Availability")
    number_available = (
        number_available_element.find_next_sibling("td").text.strip()
        if number_available_element
        else ""
    )

    description_element = soup.find("div", {"id": "product_description"})
    product_description = (
        description_element.find_next_sibling("p").text.strip()
        if description_element and description_element.find_next_sibling("p")
        else ""
    )

    category_element = soup.find(
        "a", href=lambda href: href and "category/books/" in href
    )
    category = category_element.text.strip() if category_element else ""

    review_rating_element = soup.find("p", {"class": "star-rating"})
    review_rating = (
        review_rating_element.get("class")[1] if review_rating_element else ""
    )

    image_element = soup.find("img", {"class": "thumbnail"})
    image_url = image_element.get("src") if image_element else ""

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
