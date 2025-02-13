import requests
import datetime
import math

from datetime import datetime

from unicodedata import normalize

import deep_translator
from deep_translator import GoogleTranslator

#############################################################

# API endpoint for the Albion Online data
PRICE_URL = "https://west.albion-online-data.com/api/v2/stats/prices/"

# Request the data of the current items names and descriptions from github
CURRENT_ITEMS_RESPONSE = requests.get("https://raw.githubusercontent.com/ao-data/ao-bin-dumps/refs/heads/master/formatted/items.json")

# Print According to selected Language
ASK_SEARCH = {"PT-BR":"Buscar Item: ", "EN-US":"Search Item: "}

INVALID_ENTRY = {"PT-BR":"Entrada Inválida", "EN-US":"Invalid Entry"}
NOT_FOUND = {"PT-BR":"Item Não Encontrado!", "EN-US":"Item Not Found!"}
CANT_RETRIEVE = {"PT-BR":"Não foi possível acessar os dados de Albion Market Data", 
                 "EN-US":"Can't retrive item data from Albion Market Data"}

QUIT_OPTION = {"PT-BR":"sair", "EN-US":"quit"}
SILVER = {"PT-BR":"pratas", "EN-US":"silver"}


# Use quality 0 or 2 for non-equipment items
QUALITY = '2'

# The map main locations
LOCATIONS = ['Thetford', 'Lymhurst', 'Bridgewatch', 'Martlock', 'Fort Sterling', 'Caerleon', 'Brecilien']

def get_price(PRICE_URL, ITEM_NAME, LOCATION):
    """Get the item price by Location"""

    # Request data from the Albion Online API
    current_prices_response = requests.get(PRICE_URL + ITEM_NAME + '.json?&locations=' + LOCATION)

    # Check if the request was successful
    if current_prices_response.status_code == 200:
        # Extract the market prices from the response data
        market_prices = current_prices_response.json()[0]["sell_price_min"]

        # Get the last udpate time
        time = current_prices_response.json()[0]["sell_price_min_date"]
        return {"price":market_prices, "time":time}

    else:   
        return {}
    
# Will get the item information from it's LocalizedName. e.g item UniqueName, item LocalizedDescription...
def get_item(ITEM_NAME ,LANGUAGE):
    """Get the item from it's localized name according the selected language"""

    # Check if the request was successful
    if CURRENT_ITEMS_RESPONSE.status_code == 200:
        # Extract the item descriptions from the response data
        current_items = CURRENT_ITEMS_RESPONSE.json()

        for item in current_items:
            if (item['LocalizedNames'] != None):
                # Normalize the input and the compared item name to compare them
                normalized_name = normalize("NFKD", item['LocalizedNames'][LANGUAGE]).encode('ascii', 'ignore').decode('ascii').lower()
                normalized_search = normalize("NFKD", ITEM_NAME).encode('ascii', 'ignore').decode('ascii').lower()

                # If the search is made by LocalizedName or by UniqueName
                if normalized_search in normalized_name or ITEM_NAME.upper() == item["UniqueName"]:
                    return item
    return None

def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')