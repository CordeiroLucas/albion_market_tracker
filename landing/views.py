from django.shortcuts import render, redirect
from django.utils.translation import get_language as get_language
from django.http import HttpResponse
from .scripts import library

LANGUAGE_CODE = get_language().upper()

# Create your views here.

def index(request):
    """Render the index page with the Albion Online Market Data"""
    if request.method == 'GET':
        try: 
            return render(request, 'index.html')
        except Exception as e:
            return redirect('search')


def search(request):
    """Render the search page and handle item search requests"""
    if request.method == 'GET':
        print(f"GET request received for search page {get_language()}")
        return render(request, 'search.html', {
            'ask_search': library.ASK_SEARCH[LANGUAGE_CODE],  # Change to 'PT-BR' for Portuguese
            'item_name': '',
        })
      
    if request.method == 'POST':
        item_name = request.POST.get('search_item')
        print(f"POST request received for item search: {item_name} in {get_language()}")

        item_obj = library.get_item(item_name, LANGUAGE_CODE)

        if item_obj == None:
            return HttpResponse(library.INVALID_ENTRY[LANGUAGE_CODE])
        
        item = item_handler(item_obj, LANGUAGE_CODE)

        print(f"Item found: {item['item_name']}\nDescription: {item['item_description']}\nUnique Name: {item['item_unique_name']}")
    
        item_prices = {}
        # Get the price for each location
        for location in library.LOCATIONS:
            loc_price = library.get_price(library.PRICE_URL, item['item_unique_name'], location)
            curr_price = {}
            if loc_price:
                curr_price['price'] = loc_price['price']
                curr_price['time'] = library.parse_timestamp(loc_price['time'])
            else:
                curr_price['price'] = 'N/A'
                curr_price['time'] = 'N/A'
                
            curr_price['location'] = location
            item_prices[location] = curr_price

        return render(request, 'search.html', {
            'item_name': item['item_name'],
            'item_description': item['item_description'],
            'item_unique_name': item['item_unique_name'],
            'locations': library.LOCATIONS,
            'silver': library.SILVER[LANGUAGE_CODE],
            'item_prices': item_prices.values(),
            'ask_search': library.ASK_SEARCH[LANGUAGE_CODE],
        })

def item_handler(item:dict, language:str):
    """Handle item data and return a dictionary with relevant information"""
    try:
        local_name = item['LocalizedNames'][language]
    except Exception:
        local_name = "Inválido"

    try:
        local_desc = item['LocalizedDescriptions'][language]
    except Exception:
        local_desc = "Sem Descrição"

    unique_name = item.get('UniqueName')

    return {
        'item_name': local_name,
        'item_description': local_desc,
        'item_unique_name': unique_name,
    }