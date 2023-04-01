from django.contrib.auth import get_user_model
from rest_framework import serializers

from order.models import Products, BasketProducts, Basket

User = get_user_model()


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ("__all__",)


class BasketProductsSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductsSerializer(many=True)

    class Meta:
        model = BasketProducts
        fields = ('basket', 'products')


class BasketSerializer(serializers.HyperlinkedModelSerializer):
    basket_products = BasketProductsSerializer(many=True)

    class Meta:
        model = Basket
        fields = ('user', 'basket_products ')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    basket = BasketSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'basket')
