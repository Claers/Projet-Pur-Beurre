from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="acceuil"),
    path('success', views.index, name="acceuil_login"),
    path('search', views.search, name="recherche"),
    path('connexion', views.connexion, name="connexion"),
    path('deconnexion', views.logout_user, name="logout"),
    path('product/<product_name>', views.product_info, name="produit"),
    path('product/<product_name>/<substitute_name>',
         views.product_substitute_info, name="produit_substitut"),
    path('favoris/<product_name>/<substitute_name>',
         views.register_fav, name="favoris_register"),
    path('remove/<product_name>/<substitute_name>',
         views.remove_fav, name="favoris_remove"),
    path('admin/fill', views.filldata, name="fill"),
    path('user', views.user, name="user"),
    path('favoris', views.favorites, name="favoris"),
    path('admin/delete', views.deldata, name="deleteDB"),
]
