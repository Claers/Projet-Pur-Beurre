from .models import Product, Category
import requests
import json

# Initialisation


def jsonProductList(i):
    frURL = "https://fr.openfoodfacts.org/country/france/{0}.json".format(i)

    reURl = "https://fr.openfoodfacts.org/country/reunion/{0}.json".format(
        i)
    response = requests.get(frURL)
    data = response.json()
    return data


def productCorrect(product):
    if((product['states_hierarchy'][1] == "en:complete") and
       (product['stores'] is not None) and
       (len(product['nutrition_grades']) < 2)):
        return True


def fill():
    i = 1
    products = []
    try:
        while (i <= 150):
            products = jsonProductList(i)
            for p in products['products']:
                try:
                    print(p['states_hierarchy'][1])
                    if(productCorrect(p)):
                        try:
                            productobj = Product.objects.get(
                                productName=p['product_name'])
                            if(productobj.productURL is None):
                                productobj.productURL = p["image_front_url"]
                        except Product.DoesNotExist:
                            productobj = Product.objects.create(
                                productName=p['product_name'],
                                shops=p['stores'],
                                brands=p['brands'],
                                productURL=p['url'],
                                nutriscore=p['nutrition_grades'],
                                imgURL=p['image_front_url'])
                            for category in p['categories'].split(","):
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
