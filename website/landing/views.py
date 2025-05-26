from django.shortcuts import render, HttpResponse
from . import library

# Create your views here.

def index(request):
    """Render the index page with the Albion Online Market Data"""
    if request.method == 'GET':
        return render(request, 'index.html')
    
    if request.method == 'POST':
        item_name = request.POST.get('item_name')

        item_obj = library.get_item(item_name, request.LANGUAGE_CODE)
        if item_obj == None:
            return HttpResponse(library.INVALID_ENTRY[request.LANGUAGE_CODE])
        
        return render(request, 'index.html', {
            'item_name': item_obj['LocalizedName'],
            'item_description': item_obj['LocalizedDescription'],
            'item_unique_name': item_obj['UniqueName'],
            'item_quality': item_obj['Quality'],
            'item_type': item_obj['Type'],
            'item_category': item_obj['Category'],
            'item_price': library.get_price(library.PRICE_URL, item_obj['UniqueName'], request.POST.get('location')),
            'locations': library.LOCATIONS,
        })
