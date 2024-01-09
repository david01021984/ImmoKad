import requests
import time
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

links = [ 'https://www.immoweb.be/fr/annonce/maison/a-vendre/wetteren/9230/11058079',
         'https://www.immoweb.be/fr/annonce/maison/a-vendre/marche-en-famenne/6900/11058166',
         'https://www.immoweb.be/fr/annonce/maison/a-vendre/gand/9000/11058202',
         'https://www.immoweb.be/fr/annonce/projet-neuf-maisons/a-vendre/erembodegem/9320/11057821',
         'https://www.immoweb.be/fr/annonce/projet-neuf-maisons/a-vendre/grammont/9500/11001458',
         'https://www.immoweb.be/fr/annonce/projet-neuf-maisons/a-vendre/hofstade/9308/11001463',
         'https://www.immoweb.be/fr/annonce/appartement/a-vendre/gavere/9890/11050973',
         'https://www.immoweb.be/fr/annonce/appartement/a-vendre/gavere/9890/11050978',
         'https://www.immoweb.be/fr/annonce/appartement/a-vendre/bruxelles/1000/11058606'

]

for link in links :
    # URL du site web que vous souhaitez scraper
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)
    driver.get(link)

    # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    html = soup.find("script",attrs={"type":"text/javascript"})

    # Find the script tag containing the window.classified object
    #script_tag = soup.find('script', text=lambda x: 'window.classified =' in x)

    # Extract the content of the script tag
    script_content = html.text.strip()

    # Extract the window.classified object from the script content
    start_index = script_content.find('{')
    end_index = script_content.rfind('}') + 1
    classified_json = script_content[start_index:end_index]

    # Parse the JSON data
    classified_data = json.loads(classified_json)

    # Access specific information
    property_type = classified_data['property']['type']
    property_subtype = classified_data['property']['subtype']
    region = classified_data['property']['location']['region']
    city = classified_data['property']['location']['locality']
    postal = classified_data['property']['location']['postalCode']
    showers = classified_data['property']['showerRoomCount']
    bedrooms = classified_data['property']['bedroomCount']
    bathrooms = classified_data['property']['bathroomCount']
    parkings_in = classified_data['property']['parkingCountIndoor']
    parkings_out = classified_data['property']['parkingCountOutdoor']
    garden_size = classified_data['property']['gardenSurface']

    rooms = classified_data['property']['roomCount']
    surface = classified_data['property']['netHabitableSurface']
    wc = classified_data['property']['toiletCount']

    has_basement = 1 if classified_data['property']['hasBasement'] == True else 0
    has_dressing = 1 if classified_data['property']['hasDressingRoom'] == True else 0
    has_dining_room = 1 if classified_data['property']['hasDiningRoom'] == True else 0
    is_furnished = 1 if classified_data['transaction']['sale']['isFurnished'] == True else 0
    has_swimming_pool = 1 if classified_data['property']['hasSwimmingPool'] == True else 0
    has_fire_place =  1 if classified_data['property']['fireplaceExists'] == True else 0
    has_garden = 1 if classified_data['property']['hasGarden'] == True else 0 
    has_balcony = 1 if classified_data['property']['hasBalcony'] == True else 0 

    bail = classified_data['transaction']['subtype']
    kitchen_info = classified_data['property']['kitchen']
    if kitchen_info != None:
        kitchen_type = kitchen_info['type']
    else :
        kitchen_type = None

    building = classified_data['property']['building']
    if building != None : 
        nb_facades = classified_data['property']['building']['facadeCount'] 
        building_condition = classified_data['property']['building']['condition']
    else : 
        nb_facades = None
        building_condition = None

    

    land = classified_data['property']['land']
    if land != None :
        surface_land = classified_data['property']['land']['surface']
    else : surface_land = None

    agency_name = classified_data['customers'][0]['name']
    agency_email = classified_data['customers'][0]['email']
    agency_phone = classified_data['customers'][0]['phoneNumber']
    agency_info = classified_data['customers']

    price = classified_data['transaction']['sale']['price']
    transac_info = classified_data['transaction']

    # Print the retrieved information
    print("Property Type:", property_type)
    print("Property Subtype:", property_subtype)
    print("Region :", region)
    print("City :", city)
    print("CP :", postal)



    print("Agency Name:", agency_name)
    print("Agency Email:", agency_email)
    print("Agency Phone:", agency_phone)
    print("Type de vente : ", bail)

    print("Price:", price)

    print("Nombre de façades :", nb_facades)
    print("Nombre de chambres", bedrooms)
    print("Nombre de salles de bain", bathrooms)
    print("Nombre de douches :", showers)
    print("Nombre de toilettes :", wc)
    print("Nombre de pièces :", rooms)
    print("Nombre de parking intérieurs :", parkings_in)
    print("Nombre de parking intérieurs :", parkings_out)
    print("Type de cuisine :", kitchen_type)
    print("État du bâtiment :", building_condition)
    print("Surface habitable :", surface)
    print("Surface jardin :", garden_size)
    print("Surface totale :", surface_land)
    print("Basement :", has_basement)
    print("Dressing :", has_dressing)
    print("Dining Room :", has_dining_room)
    print("Meublé :", is_furnished)
    print("Cheminée :", has_fire_place )
    print("Terrasse :", has_balcony)
    print("Jardin :", has_garden)
    print("Piscine :",has_swimming_pool )

    time.sleep(1.5)
