import requests
import datetime
from datetime import datetime
from unicodedata import normalize

ASK_SEARCH = {"PT-BR":"Buscar Item: ", "EN-US":"Search Item: "}
NOT_FOUND = {"PT-BR":"Item Não Encontrado!", "EN-US":"Item Not Found!"}
QUIT_OPTION = {"PT-BR":"sair", "EN-US":"quit"}
SILVER = {"PT-BR":"pratas", "EN-US":"silver"}

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
        print("Can't retrive item data from Albion Market Data")
        return {}
    

# Will get the item information from it's LocalizedName. e.g item UniqueName, item LocalizedDescription...
def get_item(ITEM_NAME ,LANGUAGE):
    """Get the item from it's localized name according the selected language"""

    # Request data from the Albion Online GitHub
    current_items_response = requests.get("https://raw.githubusercontent.com/ao-data/ao-bin-dumps/refs/heads/master/formatted/items.json")

    # Check if the request was successful
    if current_items_response.status_code == 200:

        # Extract the item descriptions from the response data
        current_items:list = current_items_response.json()

        for item in current_items:
            if (item['LocalizedNames'] != None):
                # Normalize the input and the compared item name to compare them
                normalized_name = normalize("NFKD", item['LocalizedNames'][LANGUAGE]).encode('ascii', 'ignore').decode('ascii').lower()
                normalized_search = normalize("NFKD", ITEM_NAME).encode('ascii', 'ignore').decode('ascii').lower()
        
                # If the search is made by LocalizedName or by UniqueName
                if normalized_search == normalized_name or ITEM_NAME.upper() == item["UniqueName"]:
                    return item
    return None

def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')