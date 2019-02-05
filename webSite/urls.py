from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="acceuil"),
    path('search', views.search, name="recherche"),
    path('connexion', views.connexion, name="connexion"),
    path('logout', views.logoutUser, name="logout"),
    path('product/<pName>', views.productInfo, name="produit"),
    path('admin/fill', views.filldata, name="fill")
]