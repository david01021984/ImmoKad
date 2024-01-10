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

i=1
tabLinks = []
while i <= 333:
    lien = (f"https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE&priceType=SALE_PRICE&page={i}")
    
    # URL du site web que vous souhaitez scraper
    url = requests.get(lien).text
    # driver = webdriver.Edge()
    # driver.get(lien)
    
    i += 1

    nbr_entree = 0


    # def enter_url():
    soup = BeautifulSoup(url, "lxml")
    brutlinks = soup.find_all("a")
    
    for brutlink in brutlinks:
        
        link = brutlink["href"]

        if "https://www.immoweb.be/fr/annonce/" in link and "projet" not in link:
            tabLinks.append(link)
        else:
            continue
           
      
    time.sleep(3)
clean_list=set(tabLinks)

current_datetime = datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

# Create the file name using the formatted date and time
 
chemin = f"url_list_{formatted_datetime}.txt"

with open(chemin, 'w') as fichier:
    # Écrire chaque élément de la liste dans une ligne du fichier
    for element in clean_list:
        fichier.write((element)+'\n')