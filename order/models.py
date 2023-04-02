from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')


class BasketProducts(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_products')
    products = models.ManyToManyField('Products', related_name="basket_products")


class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=100, decimal_places=2)
