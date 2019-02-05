from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from .forms import ConnexionForm
from django.contrib import messages
import json
import requests
from .databaseFill import fill
# Create your views here.

isLogout = False
isConnected = False
isFilled = False


def index(request):
    global isLogout, isConnected
    if(isLogout):
        messages.success(request,  "Vous avez été déconnecté.")
        isLogout = False
    if(isConnected):
        messages.success(request,  "Vous êtes connecté.")
        isConnected = False

    return render(request, 'site/index.html', locals())


def search(request):
    name = request.POST.get('PName', '')
    if(name != ""):
        try:
            isRaw = bool(request.POST.get('productRaw'))
            if(isRaw):
                product = Product.objects.get(productName=name)
            else:
                product = Product.objects.get(productName__contains=name)
            url = product.productURL
            img = product.imgURL
            substitutes = Product.objects.filter(
                productName__contains=name).exclude(
                productName=product)
            categories = product.category_set.all()
            productByCat = {}
            productAlreadyListed = []
            for category in categories:
                substitutes = (substitutes | category.products.exclude(
                    productName=product))
                for prod in productAlreadyListed:
                    substitutes = substitutes.exclude(productName=prod)
                for sub in substitutes:
                    productAlreadyListed.append(sub.productName)
                productByCat[category.categoryName] = substitutes.exclude(
                    id=product.id).order_by('nutriscore').distinct()
            return render(request, 'site/search.html', locals())
        except Product.MultipleObjectsReturned:
            products = Product.objects.filter(
                productName__contains=name).order_by('nutriscore').distinct()
            return render(request, 'site/search.html', locals())
        except Product.DoesNotExist:
            return HttpResponse("null")
    else:
        return HttpResponse("NoData")


def productInfo(request, pName):
    product = Product.objects.get(productName=pName)
    url = product.productURL
    code = url.split("/")[4]
    resp = requests.get(
        "https://fr.openfoodfacts.org/api/v0/produit/"+code+".json")
    data = resp.json()
    nutriIMG = data['product']["image_nutrition_url"]
    return render(request, 'site/product.html', locals())


def filldata(request):
    fill()
    return render(request, 'admin/base_site.html', locals())


def connexion(request):
    global isConnected
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Nous vérifions si les données sont correctes
            user = authenticate(username=username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                isConnected = True
                return redirect('acceuil')
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'site/login.html', locals())


def logoutUser(request):
    global isLogout
    logout(request)
    isLogout = True
    return redirect('acceuil')
