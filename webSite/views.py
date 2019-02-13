"""
webSite app views document
"""

from random import randint
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.admin.utils import unquote

from .models import Product, Profile, Favorite
from .forms import ConnexionForm, RegisterForm
from .database_fill import fill, delete_db


# Create your views here.

def index(request):
    """
    Display the index of the site

    Returns:
        template : "site/index.html"
    """
    current_url = request.path_info
    if "success" in current_url and not request.user.is_authenticated:
        messages.success(request, "Vous avez été déconnecté.")
    if "success" in current_url and request.user.is_authenticated:
        messages.success(request, "Vous êtes connecté.")

    return render(request, 'site/index.html', locals())


def list_product_by_category(products, categories, exclude_product):
    """Function used to list products by categories and for remove duplicates

    Arguments:
        products {list of Product} -- The list of products you want to order
        categories {list of Category} -- The list of categories of your product
        exclude_product {Product} -- The original product to exclude

    Returns:
        products_by_category {dict} -- The products ordered by categorie and
        nutriscore
    """
    product_already_listed = []
    products_by_category = {}
    for category in categories:
        products = (products | category.products.exclude(
            productName=exclude_product))
        for product in product_already_listed:
            products = products.exclude(productName=product)
        for product in products:
            product_already_listed.append(product.productName)
        products_by_category[category.categoryName] = products.exclude(
            id=exclude_product.id).order_by('nutriscore').distinct()
    return products_by_category


def search(request):
    """Display the page for product search

    Models:
        Product, Category

    Returns:
        template : "site/search.html"
    """
    name = request.POST.get('product_name', '')
    random_img = randint(1, 3)
    if name != "":
        try:
            is_raw = bool(request.POST.get('productRaw'))
            name = unquote(name)
            if is_raw:
                product = Product.objects.get(productName=name)
            else:
                product = Product.objects.get(productName__icontains=name)
            url = product.productURL
            img = product.imgURL
            substitutes = Product.objects.filter(
                productName__icontains=name).exclude(
                    productName=product)
            categories = product.category_set.all()
            products_by_category = list_product_by_category(
                substitutes, categories, product)
            return render(request, 'site/search.html', locals())
        except Product.MultipleObjectsReturned:
            products = Product.objects.filter(
                productName__icontains=name).order_by('nutriscore').distinct()
            return render(request, 'site/search.html', locals())
        except Product.DoesNotExist:
            return render(request, 'site/search.html', locals())
    else:
        messages.error(
            request, "Pour faire une recherche, merci d'entrer un aliment.")
        return render(request, 'site/index.html', locals())


def product_info(request, product_name):
    """Display the page of a product

    Arguments:
        product_name {string} -- The name of the product

    Models:
        Product

    Returns:
        template : "site/product.html"
    """

    random_img = randint(1, 3)
    product_name = unquote(product_name)
    product = Product.objects.get(productName=product_name)
    url = product.productURL
    code = url.split("/")[4]
    resp = requests.get(
        "https://fr.openfoodfacts.org/api/v0/produit/"+code+".json")
    data = resp.json()
    nutri_img = data['product']["image_nutrition_url"]
    return render(request, 'site/product.html', locals())


def product_substitute_info(request, product_name, substitute_name):
    """Display the page of a product from a substitute search

    Arguments:
        product_name {string} -- The name of the product
        substitute_name {string} -- The name of the substitute

    Returns:
        template : "site/product.html"
    """
    random_img = randint(1, 3)
    product_name = unquote(product_name)
    substitute_name = unquote(substitute_name)
    product = Product.objects.get(productName=product_name)
    substitute = Product.objects.get(productName=substitute_name)
    url = substitute.productURL
    code = url.split("/")[4]
    resp = requests.get(
        "https://fr.openfoodfacts.org/api/v0/produit/"+code+".json")
    data = resp.json()
    nutri_img = data['product']["image_nutrition_url"]
    return render(request, 'site/product.html', locals())


def user(request):
    """Display the user page

    Returns:
        template : "site/user.html"
    """

    if request.user.is_authenticated:
        random_img = randint(1, 3)
        username = None
        if request.user.is_authenticated:
            username = request.user.username
            email = request.user.email
        return render(request, 'site/user.html', locals())
    else:
        return redirect('connexion')


def favorites(request):
    """Display the favorite page of user

    Models:
        Favorite

    Returns:
        template : "site/favoris.html"
    """

    random_img = randint(1, 3)
    if request.user.is_authenticated:
        profile = request.user.profile
        favorites = profile.favorites.all()
        return render(request, 'site/favoris.html', locals())
    else:
        pass


def register_fav(request, product_name, substitute_name):
    """View used to register a favorite in user profile

    Arguments:
        product_name {string} -- The name of the product
        substitute_name {string} -- The name of the substitute

    Models:
        Product, Favorite

    Returns:
        template : "site/favoris.html"
    """
    random_img = randint(1, 3)
    if request.user.is_authenticated:
        profile = request.user.profile
        favorites = profile.favorites.all()
        try:
            product = Product.objects.get(productName=product_name)
        except Product.DoesNotExist:
            messages.error(
                request, "Le produit sélectionné n'as pas été trouvé.")
            return render(request, 'site/favoris.html', locals())
        try:
            substitute = Product.objects.get(productName=substitute_name)
        except Product.DoesNotExist:
            messages.error(
                request, "Le produit sélectionné n'as pas été trouvé.")
            return render(request, 'site/favoris.html', locals())
        fav = Favorite(product=product, substitute=substitute)
        try:
            favorite = Favorite.objects.get(
                product=product, substitute=substitute)
            try:
                profile.favorites.get(product=product, substitute=substitute)
                messages.error(
                    request, "Favori déja existant")
            except profile.DoesNotExist:
                profile.favorites.add(fav)
                messages.success(request, "Favori bien enregistré")
        except Favorite.DoesNotExist:
            favorite = None
            fav.save()
            profile.favorites.add(fav)
            messages.success(request, "Favori bien enregistré")
        favorites = profile.favorites.all()
        return render(request, 'site/favoris.html', locals())
    else:
        return redirect('connexion')


def remove_fav(request, product_name, substitute_name):
    """View used to remove a favorite in user profile

    Arguments:
        product_name {string} -- The name of the product
        substitute_name {string} -- The name of the substitutes

    Models:
        Product, Favorite

    Returns:
        template : "site/favoris.html"
    """
    random_img = randint(1, 3)
    if request.user.is_authenticated:
        profile = request.user.profile
        product = Product.objects.get(productName=product_name)
        substitute = Product.objects.get(productName=substitute_name)
        try:
            userfav = profile.favorites.get(
                product=product, substitute=substitute)
            userfav.delete()
            messages.success(request, "Favori supprimé !")
        except Favorite.DoesNotExist:
            messages.error(
                request, "Ce favori n'existe pas.")
        favorites = profile.favorites.all()
        return render(request, 'site/favoris.html', locals())
    else:
        return redirect('connexion')


def connexion(request):
    """Display the connection page and connect or register a user.

    Returns:
        template : "site/login.html"
    """
    random_img = randint(1, 3)
    if request.user.is_authenticated:
        messages.error(request, "Vous êtes déja connecté !")
        return render(request, 'site/index.html', locals())
    if bool(request.POST.get('connect', '')):
        if request.method == "POST":
            form = ConnexionForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                # Nous vérifions si les données sont correctes
                user = authenticate(username=username,
                                    password=password)
                if user:  # Si l'objet renvoyé n'est pas None
                    login(request, user)  # nous connectons l'utilisateur
                    return redirect('acceuil_login')
                else:  # sinon une erreur sera affichée
                    messages.error(request,
                                   "Utilisateur inconnu ou" +
                                   " mauvais de mot de passe.")
            else:
                messages.error(request,
                               "Utilisateur inconnu ou" +
                               " mauvais de mot de passe.")
    else:
        try:
            if request.method == "POST":
                form = RegisterForm(request.POST)
                if form.is_valid():
                    username = request.POST.get("username", '')
                    password = request.POST.get("password", '')
                    email = request.POST.get("email", '')
                    # Nous vérifions si les données sont correctes
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email)
                    Profile.objects.create(
                        user=user, email=email, favorites=None)
                    user = authenticate(username=username,
                                        password=password)
                    if user:  # Si l'objet renvoyé n'est pas None
                        login(request, user)  # nous connectons l'utilisateur
                        return redirect('acceuil_login')
                else:
                    messages.error(request, "Merci de remplir tout les champs")
        except IntegrityError:
            messages.error(request,
                           "Utilisateur déja existant")

    return render(request, 'site/login.html', locals())


def legal_mentions(request):
    """
    Display the legal mentions page
    """
    return render(request, 'site/legal.html', locals())


def logout_user(request):
    """View used to logout a user

    Returns:
        redirect to "site/index.html"
    """
    logout(request)
    return redirect('acceuil_login')


def filldata(request):
    """View used to launch the database fill function

    It can be accessed in template with that view
    But it will only be used on admin templates

    Returns:
        template : "admin/base_site.html"
    """
    fill_thread = fill()
    fill_thread.start()
    return render(request, 'admin/base_site.html', locals())


def deldata(request):
    """View used to launch the database delete function

    It can be accessed in template with that view
    But it will only be used on admin templates

    Returns:
        template : "admin/base_site.html"
    """
    delete_db()
    return render(request, 'admin/base_site.html', locals())
