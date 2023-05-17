import csv
import os
import requests
from urllib.parse import urljoin


def download_images(filename, fieldnames):
    image_directory = "images"
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        next(reader)  # Ignorer la première ligne (titres de colonnes)

        # Parcourir les lignes du fichier CSV
        for row in reader:
            image_url = row["image_url"]

            # Vérifier si l'URL de l'image existe
            if image_url:
                # Construire le chemin de destination pour l'image en utilisant le titre du livre comme nom de fichier
                image_filename = f"{row['upc']}.jpg"
                image_path = os.path.join(image_directory, image_filename)

                # Enregistrer l'image
                save_image_from_url(image_url, image_path)


def save_image_from_url(image_url, destination_path):
    base_url = "https://books.toscrape.com/"
    final_url = urljoin(base_url, image_url)
    response = requests.get(final_url)
    response.raise_for_status()

    with open(destination_path, "wb") as file:
        file.write(response.content)
