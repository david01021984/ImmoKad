import requests
import csv
from datetime import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

tabLinks = []

def fetch_links(page_number):
    lien = f"https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&priceType=SALE_PRICE&page={page_number}"
    
    # Obtenir le contenu de la page
    response = requests.get(lien)
    soup = BeautifulSoup(response.text, "lxml")

    brutlinks = soup.find_all("a")

    for brutlink in brutlinks:
        link = brutlink.get("href", "")

        if "https://www.immoweb.be/fr/annonce/" in link and "projet" not in link:
            tabLinks.append(link)

    time.sleep(0.2)

def main():
    num_threads = 16
    # Nombre de pages à parcourir
    num_pages = 220

    # Utiliser ThreadPoolExecutor pour paralléliser le travail
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Soumettre les tâches à l'exécuteur pour chaque page
        executor.map(fetch_links, range(1, num_pages))

    # Supprimer les doublons de la liste
    clean_list = set(tabLinks)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    chemin = f"url_list_{formatted_datetime}.txt"

    with open(chemin, 'w') as fichier:
        for element in clean_list:
            fichier.write((element) + '\n')

if __name__ == "__main__":
    main()
