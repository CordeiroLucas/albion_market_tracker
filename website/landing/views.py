from django.shortcuts import render, HttpResponse
from . import library

# Create your views here.

def index(request):
    return render(request, 'index.html')