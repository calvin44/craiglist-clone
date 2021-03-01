from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from . import models


BASE_CRAIGLIST_URL = "https://losangeles.craigslist.org/search/?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# function to concat string


def stringConcat(a):
    if a == None:
        return ""
    else:
        return "%20".join(a.split(" "))


def home(request):
    return render(request, 'base.html')


def new_search(request):

    # get user input
    search = request.POST.get('search')

    # save search to database
    models.Search.objects.create(search=search)

    # construct url for web scrapping
    final_url = BASE_CRAIGLIST_URL.format(stringConcat(search))

    # web scrapping part
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    # get element
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(
                class_='result-image').get('data-ids').split(',')[0][2:]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craislist.org/images/peace.jpg'
        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    # data to be passed to front end
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
