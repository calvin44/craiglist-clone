from django.shortcuts import render
from bs4 import BeautifulSoup
import requests


# Create your views here.


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # get the posted data from the form
    # parameters = form input name
    search = request.POST.get('search')
    stuff_for_frontend = {
        'search': search
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
