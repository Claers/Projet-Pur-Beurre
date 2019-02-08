"""
Models of the webSite app objects
"""

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    """Store a product
    The product is unique

    Fields:
        productName {CharField} -- The name of the product (max_lenght=100)
        shops {TextField} -- The shops of the product (null=False)
        brands {TextField} -- The brands of the product (null=False)
        productURL {URLField} -- The url of the product
        nutriscore {CharField} -- The nutriscore of the product (max_lenght=1)
        imgURL {URLField} -- The url of the product image

    Returns:
       self.productName {string} -- The name of the product
    """
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
    substitute = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='%(class)s_substitute')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='%(class)s_product')

    def __str__(self):
        return ("Substitut : " + str(self.substitute)
                + " / Produit : " + str(self.product))

    class Meta:
        verbose_name = "Favoris"
        verbose_name_plural = "Favoris"
        ordering = ['product']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        Favorite)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)
