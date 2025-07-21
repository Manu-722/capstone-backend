from django.contrib import admin
from .models import Shoe, CartItem, Order
from django.utils.html import format_html

@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'in_stock', 'category', 'created_at', 'image_preview']
    search_fields = ['name']
    list_filter = ['in_stock', 'category']
    fields = ['name', 'price', 'category', 'sizes', 'image', 'description', 'in_stock', 'created_at']
    readonly_fields = ['created_at', 'image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" style="object-fit:cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'shoe', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'shoe__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'payment_method', 'paid', 'status', 'created_at']
    list_filter = ['payment_method', 'paid', 'status']
    search_fields = ['user__username']
    readonly_fields = ['total', 'created_at']