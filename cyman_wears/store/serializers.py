from rest_framework import serializers
from .models import Shoe, CartItem

class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    shoe = ShoeSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'shoe', 'quantity', 'get_total_price', 'get_discounted_price']