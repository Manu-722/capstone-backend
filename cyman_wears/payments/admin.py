from django.contrib import admin
from .models import PaymentTransaction

# Register your models here.
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'amount', 'transaction_id', 'timestamp')
    search_fields = ('name', 'phone', 'transaction_id')
