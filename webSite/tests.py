from django.test import TestCase, Client
from .models import Product, Category

# Create your tests here.


class ProductModelTest(TestCase):
    def test_string_representation(self):
        product = Product(productName="Pizza")
        self.assertEqual(str(product), product.productName)


class TestSearch(TestCase):

    def test_search_one_object(self):
        client = Client()
        Product.objects.create(productName="Test")
        response = client.post(
            '/search', {"product_name": "Test"}, follow=True)
        self.assertContains(response, "Test")

    def test_find_substitute(self):
        client = Client()
        obj1 = Product.objects.create(
            productName="Test", productURL="http://test.com")
        obj2 = Product.objects.create(
            productName="Test2", productURL="http://test2.com")
        category = Category.objects.create(categoryName="categoryTest")
        category.products.add(obj1)
        category.products.add(obj2)
        response = client.post(
            '/search', {"product_name": "Test2"}, follow=True)
        self.assertEqual(
            response.context['productByCat']['categoryTest'][0], obj1)
