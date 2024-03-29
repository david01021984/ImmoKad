import requests
from datetime import datetime
import os
import pandas as pd
import time
from bs4 import BeautifulSoup
import json
import random
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


def creer_dossier(chemin_dossier):
    # Vérifier si le dossier existe
    if not os.path.exists(chemin_dossier):
        # Créer le dossier s'il n'existe pas
        os.makedirs(chemin_dossier)
        print(f"Dossier '{chemin_dossier}' créé avec succès.")
    else:
        print(f"Dossier '{chemin_dossier}' existe déjà.")


# Get the current date and time
current_datetime = datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

chemin_dossier = "./RECORDS"
creer_dossier(chemin_dossier)

# Create the file name using the formatted date and time
csv_file_name = rf'RECORDS/records_{formatted_datetime}.csv'


#This function retrieve the latest url_list text file created
def get_latest_file_with_prefix(prefix):
    list_of_files = [file for file in os.listdir() if file.startswith(prefix)]
    full_path_files = [os.path.abspath(file) for file in list_of_files]
    
    if not full_path_files:
        return None  # No file with the specified prefix found

    # Sort files by creation time (in reverse order to get the most recent first)
    latest_file = max(full_path_files, key=os.path.getctime)

    return latest_file

prefix_to_search = "url_list"
latest_file_path = get_latest_file_with_prefix(prefix_to_search)

if latest_file_path:
    print(f"The latest file starting with '{prefix_to_search}' is: {latest_file_path}")
else:
    print(f"No file starting with '{prefix_to_search}' found in the current directory.")


# Open the file in read mode
with open(latest_file_path, 'r') as file:
    # Read each line and strip newline characters
    links = [line.strip() for line in file]


def process_link(link):
    try:
        # Fetch HTML content using requests
        response = requests.get(link)

        if response.status_code == 200:

            # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
            soup = BeautifulSoup(response.text, 'html.parser')

            html = soup.find("script",attrs={"type":"text/javascript"})

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
            has_terrasse = 1 if classified_data['property']['hasTerrace'] == True else 0

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
                "Balcon": [has_balcony],
                "Terrasse":[has_terrasse],
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
                # Save to CSV only the value without header
                df.to_csv(csv_file_name, mode = 'a',header=False, index=False)

        
            time.sleep(random.uniform(0.01,0.04))
        
        else:
                print(f"Failed to fetch content for URL: {link}")

    except Exception as e:
        print(f"An error occurred while processing {link}: {e}")

# Number of threads to use
num_threads = 24

t = time.time()

# Using ThreadPoolExecutor to parallelize the job
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    
    # Submit tasks to the executor for each link
    futures = [executor.submit(process_link, link) for link in links]

    # Wait for all tasks to complete
    for future in futures:
        future.result()  # This will raise an exception if an exception occurred in the thread

f = time.time()   
print("temps", t-f)