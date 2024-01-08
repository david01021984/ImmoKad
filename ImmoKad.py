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


# Trouver le tableau par sa classe
tables = soup.find_all('tr', class_='classified-table__row')
for table in tables:
    header = table.find("th", class_="classified-table__header")
    #print(header)
    if header :
        if header.text == "Surface du terrain":
            superficie = table.find("td",class_="classified-table__data")
            clean_superficie = (superficie.text.strip()).split(' ', 1)[0]
                                                                            
            try:
                print(f"Superficie : {clean_superficie}")
                #print(superficie)
            
            except AttributeError:
                print("Vide et none")
            #print(table.td)
                
        if header.text == "Chambres":
            nb_chambres = table.find("td",class_="classified-table__data")
            try :
                print(f"Nombre de chambres : {nb_chambres.text.strip()}")
            except AttributeError:
                print("Vide et none")

        if header.text == "Toilettes":
            nb_wc = table.find("td",class_="classified-table__data")
            try :
                print(f"Nombre de toilettes : {nb_wc.text.strip()}")
            except AttributeError:
                print("Vide et none")

    
  
