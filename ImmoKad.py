import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# URL du site web que vous souhaitez scraper
url = "https://www.immoweb.be/fr/annonce/maison/a-vendre/uccle/1180/11037509"
driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.get(url)

# Utiliser BeautifulSoup pour analyser le contenu HTML de la page
soup = BeautifulSoup(driver.page_source, 'html.parser')

def scrapFor(word):
        if header.text == word:
            x = table.find("td",class_="classified-table__data")
            try :
                print(f"{word} : {x.text.strip()}")
            except AttributeError:
                print("Vide et none")

def scrapForSplit(word):
    if header.text == word:
            x = table.find("td",class_="classified-table__data")
            clean_x = (x.text.strip()).split(' ', 1)[0]                                                                          
            try:
                print(f"{word} : {clean_x.strip()}")
            except AttributeError:
                print("Vide et none")

# Trouver le tableau par sa classe
tables = soup.find_all('tr', class_='classified-table__row')
#print(tables)
for table in tables:
    #print(table)
    print("#######")
    header = table.find("th", class_="classified-table__header")
    if header:
        print(header.text)
        data = table.find("td")
        print(data.text)

    if header :
        scrapForSplit("Surface du terrain")
        scrapForSplit("Surface du jardin")
        scrapForSplit("Surface habitable")
        scrapForSplit("Surface du salon")
        scrapForSplit("Surface de la cuisine")
        scrapForSplit("Surface du bureau")

        scrapFor("Chambres")        
        scrapFor("Classe énergétique")
        scrapFor("Toilettes")
        scrapFor("Salles de bains")
        scrapFor("Salles de douche")
        scrapFor("Nombre de façades")
        scrapFor("État du bâtiment")
        scrapFor("À partir de")
        scrapFor("Disponible le")
        scrapFor("Type de cuisine")
        scrapFor("Surface de la cuisine")
        scrapFor("Parkings intérieurs")
        scrapFor("Parkings extérieurs")
        scrapFor("Terrasse")
        scrapFor("Meublé")
        scrapFor("Bureau")



tables = soup.find_all('div', class_="classified__header-content")

for table in tables:
    #print(table)

    header = table.find("th", class_="classified-table__header")
    key = table.find("p",class_="classified__price")
    price = (key.text.strip()).split(' ', 1)[0]
    print(f"Le prix : {price.strip()}")

    address = table.find("span",class_="classified__information--address-row")
    
    localite = table.find("span",{"aria-hidden":"true"})
    clean_loc = (address.text.strip()).split(' ',1)[0]
    print(f"Adresse : {clean_loc.strip()}")

    type_de_batiment = table.find("div",class_="classified__header-primary-info")
    clean_bat = (type_de_batiment.h1.text.strip()).split(' ',1)[0]
    print(f"Type de batiment : {clean_bat.strip()}")


tables = soup.find_all('tr', class_='classified-table__row')
    
  
