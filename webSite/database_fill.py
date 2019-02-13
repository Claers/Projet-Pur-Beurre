"""Module used to fill a database from the OpenFoodFacts API

Django website app is required

Django models used : Product, Category, Favorite
"""

import requests
from .models import Product, Category, Favorite
from threading import Thread
from django.shortcuts import redirect

# Initialisation


def json_products_list(page_number):
    """Function used to create a json list of a OpenFoodFacts data page

    Arguments:
        page_number {integer} -- The number of the page that will be loaded

    Returns:
        data {json} -- The json object that contains OpenFoodFacts data
    """

    url_fr = "https://fr.openfoodfacts.org/country/france/{0}.json".format(
        page_number)

    response = requests.get(url_fr)
    data = response.json()
    return data


def product_correct(product):
    """Function used to verify if the product can be insered in database
    It check that the product as the required tags and that is complete

    Arguments:
        product {json} -- The product json object

    Returns:
        {bool} -- If true the product can be added to database
    """

    if((product['states_hierarchy'][1] == "en:complete") and
       (product['stores'] is not None) and
       (len(product['nutrition_grades']) < 2)):
        return True
    else:
        return False


class fill(Thread):
    """Function used to fill the database
    The function is made of a loop that will load 150 pages of OOF API

    Django webSite models used : Product, Category
    """

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        i = 1
        products = []
        try:
            while i <= 1:
                products = json_products_list(i)
                for product in products['products']:
                    try:
                        if product_correct(product):
                            try:
                                productobj = Product.objects.get(
                                    productName=product['product_name'])
                                if productobj.productURL is None:
                                    productobj.productURL = (
                                        product["image_front_url"])
                            except Product.DoesNotExist:
                                productobj = Product.objects.create(
                                    productName=product['product_name'],
                                    shops=product['stores'],
                                    brands=product['brands'],
                                    productURL=product['url'],
                                    nutriscore=product['nutrition_grades'],
                                    imgURL=product['image_front_url'])
                                for category in product['categories'].split(","):
                                    # SQL request to register a Categorie
                                    try:
                                        cat = Category.objects.get(
                                            categoryName=category).products.add(
                                                productobj)
                                    except Category.DoesNotExist:
                                        cat = Category.objects.create(
                                            categoryName=category)
                                        cat.products.add(
                                            productobj)

                    except KeyError:
                        continue
                i += 1

        finally:
            pass


def delete_db():
    """Function used to clear database

    Django webSite models used : Product, Category, Favorite
    """

    Category.objects.all().delete()
    Favorite.objects.all().delete()
    Product.objects.all().delete()
