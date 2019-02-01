from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from .forms import ConnexionForm
from django.contrib import messages
# Create your views here.

isLogout = False
isConnected = False


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
            product = Product.objects.get(productName__contains=name)
            return HttpResponse(str(product))
        except Product.MultipleObjectsReturned:
            products = Product.objects.filter(productName__contains=name)
            return HttpResponse(products)
        except Product.DoesNotExist:
            return HttpResponse("null")
    else:
        return HttpResponse("NoData")


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
