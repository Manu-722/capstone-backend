from rest_framework import serializers
from .models import Shoe, CartItem

class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'  

class CartItemSerializer(serializers.ModelSerializer):
    shoe = ShoeSerializer()
    get_total_price = serializers.SerializerMethodField()
    get_discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'shoe', 'quantity', 'get_total_price', 'get_discounted_price']

    def get_total_price(self, obj):
        return obj.total_price()

    def get_discounted_price(self, obj):
        return obj.discounted_price()