from django.test import TestCase, Client
from .models import Product

# Create your tests here.


class ProductModelTest(TestCase):
    def test_string_representation(self):
        product = Product(productName="Pizza")
        self.assertEqual(str(product), product.productName)


class TestSearch(TestCase):

    def test_search_one_object(self):
        c = Client()
        Product.objects.create(productName="Test")
        response = c.post('/search', {"PName": "Test"}, follow=True)
        self.assertContains(response, "Test")
