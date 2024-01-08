import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# URL du site web que vous souhaitez scraper
url = "https://www.immoweb.be/fr/annonce/ferme/a-vendre/malle/2390/11051451"
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
        if header.text == "Surface du terrain":
            superficie = table.find("td",class_="classified-table__data")
            clean_superficie = (superficie.text.strip()).split(' ', 1)[0]
                                                                            
            try:
                print(f"Superficie : {clean_superficie.strip()}")
                #print(superficie)
            
            except AttributeError:
                print("Vide et none")
            #print(table.td)

        scrapFor("Chambres")        
        scrapFor("Classe énergétique")
        scrapFor("Toilettes")
        scrapFor("Nombre de façades")
        scrapFor("État du bâtiment")
        scrapFor("À partir de")


        

    
  
