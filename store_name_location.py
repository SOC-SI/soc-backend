#HOW TO USE: prvi agrument je ime trgovine (hofer, spar, mercator), drugi je lokacija (maribor, maribor blizu xx,..), 
#output je json file lokacij in naslovov teh trgovin, scrapa od odpiralnicasi.si, naj bi bili tudi sortirani po oddaljenosti če je navedena lokacija

import requests
from bs4 import BeautifulSoup
import hashlib
import json
import sys

def get_address(street_address, postal_code, locality):
    if(street_address is not None and postal_code is not None and locality is not None):
        return street_address + ", " + postal_code + ", " + locality + ", Slovenia"
    elif(postal_code is None or postal_code == ""):
        return street_address + ", " + locality + ", Slovenia"
    elif(locality is None or locality == ""):
        return street_address + ", " + locality + ", Slovenia"
    return street_address + ", " + postal_code + ", " + locality + ", Slovenia"


def generate_unique_id(input_string):
    # Create a hash object using the SHA-256 algorithm
    hash_object = hashlib.sha256()

    # Convert the input string to bytes and update the hash object
    hash_object.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash digest
    hash_hex = hash_object.hexdigest()

    # Convert the hexadecimal hash to a decimal number
    decimal_id = int(hash_hex, 16)

    # Return the decimal ID
    return str(decimal_id)[0:16]

def remove_duplicates(data):
    # Create a new list to store unique elements
    unique_data = []
    # Iterate over each element in the data list
    for element in data:
        # Check if the current element has a unique lat and lng

        if all(element['address'].lower() != other['address'].lower() for other in unique_data):
            # Add the unique element to the new list
            unique_data.append(element)

    return unique_data

def get_stores_on_page(page, store_name):
    # url = "https://odpiralnicasi.com/spots?loc=" + your_location + "&page="+ str(page) +"&q=" + store_name + "&utf8=%E2%9C%93"
    url = "https://odpiralnicasi.com/spots?page=" + str(page) + "&q=" + store_name + "&utf8=%E2%9C%93"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    spot_wrappers = soup.find_all('div', class_='spotwrapper')



    data = []
    # Iterate over each spotwrapper div
    for spot_wrapper in spot_wrappers:
        if spot_wrapper is None:
            return data
        # Find the street address, postal code, and locality elements
        street_address = spot_wrapper.find('span', class_='street-address').text.strip()
        postal_code = spot_wrapper.find('span', class_='postal-code').text.strip()
        locality = spot_wrapper.find('span', class_='locality').text.strip()
        latitude = spot_wrapper.find('span', class_='latitude').text.strip()
        longitude = spot_wrapper.find('span', class_='longitude').text.strip()
        check_name = spot_wrapper.find('span', class_='url').text.strip()

        uniqe_id = generate_unique_id(street_address)
        naslov = get_address(street_address,postal_code,locality)

        spot_data = {
            "id": uniqe_id,
            "storeType": store_name,
            "address": naslov,
            "_geo": {
                "lat": latitude,
                "lng": longitude
            }
        }
        if(store_name not in check_name):
            continue

        data.append(spot_data)
    return data



args = sys.argv
store_name = "hofer"
your_location = "maribor"

if(len(args) > 1):
    store_name = sys.argv[1]
    your_location = sys.argv[2]

url = "https://odpiralnicasi.com/spots?utf8=%E2%9C%93&q="+ store_name + "&loc=" + your_location
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

spot_wrappers = soup.find_all('div', class_='spotwrapper')

data = []
# Iterate over each spotwrapper div
for spot_wrapper in spot_wrappers:
    # Find the street address, postal code, and locality elements
    street_address = spot_wrapper.find('span', class_='street-address').text.strip()
    postal_code = spot_wrapper.find('span', class_='postal-code').text.strip()
    locality = spot_wrapper.find('span', class_='locality').text.strip()
    latitude = spot_wrapper.find('span', class_='latitude').text.strip()
    longitude = spot_wrapper.find('span', class_='longitude').text.strip()

    uniqe_id = generate_unique_id(street_address)
    naslov = get_address(street_address,postal_code,locality)

    spot_data = {
        "id": uniqe_id,
        "storeType": store_name,
        "address": naslov,
        "_geo": {
            "lat": latitude,
            "lng": longitude
        }
    }

    data.append(spot_data)

# FOR GETTING ALL PAGES
# tmp_data = []
# for i in range(1,13):
#     tmp_data.append(get_stores_on_page(i,store_name))
#     for el in tmp_data:
#         data.extend(el)
#     tmp_data.clear()


data = remove_duplicates(data)
# Convert the data to JSON
json_data = json.dumps(data, indent=2)

with open("data.json", "w", encoding='utf-8') as file:
    # Write JSON data to the file
    json.dump(data, file, indent=2, ensure_ascii=False)


# print(json_data)

# Print the extracted information
# print('Street Address:', street_address)
# print('Postal Code:', postal_code)
# print('Locality:', locality)
# print('Lat:', latitude)
# print('Long:', longitude)
# print('----------------------')