from library import *

# The item names you want to get te market prices for
# https://github.com/ao-data/ao-bin-dumps/blob/master/formatted/items.txt

# Choose the language search
LANGUAGE = input('Select Language (e.g EN-US): ').upper()

item_to_check = ''
while item_to_check != QUIT_OPTION[LANGUAGE]:
    item_to_check = input(ASK_SEARCH[LANGUAGE])

    if get_item(item_to_check, LANGUAGE) == None and item_to_check != QUIT_OPTION[LANGUAGE]:
        print(NOT_FOUND[LANGUAGE])
    elif item_to_check != QUIT_OPTION[LANGUAGE]:
        ITEM = get_item(item_to_check, LANGUAGE)

        print()
        print(ITEM['LocalizedNames'][LANGUAGE], ITEM['UniqueName'])

        for city in LOCATIONS:
            item_info = get_price(PRICE_URL, ITEM['UniqueName'], city)
            
            print(f"{city} | {item_info['price']} {SILVER[LANGUAGE]} | {parse_timestamp(item_info['time'])}")
        print()

# print(CURRENT_PRICE_DATA)