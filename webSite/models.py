from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    productName = models.CharField(max_length=100, unique=True)
    shops = models.TextField(null=False)
    brands = models.TextField(null=False)
    productURL = models.URLField(verbose_name="URL du produit", unique=True)
    nutriscore = models.CharField(max_length=1)
    imgURL = models.URLField(
        verbose_name="URL de l'image du produit", null=True)

    def __str__(self):
        return self.productName

    class Meta:
        verbose_name = "Produit"
        ordering = ['productName']


class Category(models.Model):
    categoryName = models.CharField(max_length=150, unique=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.categoryName

    class Meta:
        verbose_name = "Catégorie"
        ordering = ['categoryName']


class Favorite(models.Model):
    substitueID = models.IntegerField(verbose_name="ID du substitut")
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return ("ID du substitut : " + str(self.substitueID)
                + " ID du produit : " + str(self.productID.id))

    class Meta:
        verbose_name = "Favoris"
        verbose_name_plural = "Favoris"
        ordering = ['productID']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    favorites = models.ForeignKey(Favorite, on_delete=models.CASCADE)

    def __str__(self):
        return "Profil de {0}".format(self.username)
