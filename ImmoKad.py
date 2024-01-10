import requests
from datetime import datetime
import os
import pandas as pd
import time
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# Get the current date and time
current_datetime = datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

# Create the file name using the formatted date and time
csv_file_name = rf'RECORDS/records_{formatted_datetime}.csv'

# # Get the current script's directory
# script_directory = os.path.dirname(os.path.abspath(__file__))

# # Specify the relative path to the urls.txt file
# file_path = os.path.join(script_directory, csv_file_name)


# Open the file in read mode
with open('url_list.txt', 'r') as file:
    # Read each line and strip newline characters
    links = [line.strip() for line in file]

# Print the list of URLs
print(links)


for link in links :
    # URL du site web que vous souhaitez scraper
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
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


    # Creating a DataFrame
    data = {
        "Property Type": [property_type],
        "Property Subtype": [property_subtype],
        "Region": [region],
        "City": [city],
        "CP": [postal],
        "Agency Name": [agency_name],
        "Agency Email": [agency_email],
        "Agency Phone": [agency_phone],
        "Type de vente": [bail],
        "Price": [price],
        "Nombre de façades": [nb_facades],
        "Nombre de chambres": [bedrooms],
        "Nombre de salles de bain": [bathrooms],
        "Nombre de douches": [showers],
        "Nombre de toilettes": [wc],
        "Nombre de pièces": [rooms],
        "Nombre de parking intérieurs": [parkings_in],
        "Nombre de parking extérieurs": [parkings_out],
        "Type de cuisine": [kitchen_type],
        "État du bâtiment": [building_condition],
        "Surface habitable": [surface],
        "Surface jardin": [garden_size],
        "Surface totale": [surface_land],
        "Basement": [has_basement],
        "Dressing": [has_dressing],
        "Dining Room": [has_dining_room],
        "Meublé": [is_furnished],
        "Cheminée": [has_fire_place],
        "Terrasse": [has_balcony],
        "Jardin": [has_garden],
        "Piscine": [has_swimming_pool],
    }

    # Check if the file exists
    file_exists = os.path.isfile(csv_file_name)


    df = pd.DataFrame(data)

    # Save the header only if the file doesn't exist
    if not file_exists:
        df.to_csv(csv_file_name, header=True, index=False)
    else :
        # Save to CSV
        df.to_csv(csv_file_name, mode = 'a',header=False, index=False)

   
    time.sleep(0.2)
    driver.quit()