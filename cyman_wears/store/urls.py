from django.urls import path
from .views import get_shoes, get_cart, add_to_cart, landing
from . import views

urlpatterns = [
    path('', landing),
    path('shoes/', get_shoes),
    path('cart/', get_cart),
    path('cart/add/', add_to_cart),
]