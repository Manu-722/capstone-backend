from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.
@csrf_exempt
def mpesa_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        amount = data.get('amount')
        # Simulate success
        return JsonResponse({'message': f'M-Pesa payment of KES {amount} from {phone} successful'})
