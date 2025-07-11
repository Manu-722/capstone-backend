from django.urls import path
from .views import mpesa_payment

urlpatterns = [
    path('mpesa/', mpesa_payment),
]