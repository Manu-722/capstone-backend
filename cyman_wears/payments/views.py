from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, requests, datetime, base64
from payments.utils.daraja import get_access_token

@csrf_exempt
def checkout_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Order received:", json.dumps(data, indent=2))
            return JsonResponse({'message': 'Order received successfully'}, status=200)
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def initiate_stk_push(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        body = json.loads(request.body)
        phone = body.get('phone')
        amount = int(body.get('amount'))

        if not phone or not amount:
            return JsonResponse({'error': 'Phone number and amount are required'}, status=400)

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        shortcode = '174379'
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        password = base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode()

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": shortcode,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/api/payments/callback/",
            "AccountReference": "CymanOrder",
            "TransactionDesc": "Cyman Wear Payment"
        }

        token = get_access_token()
        if not token:
            return JsonResponse({'error': 'Failed to retrieve access token'}, status=500)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers=headers
        )

        return JsonResponse(response.json())

    except Exception as e:
        print("STK Push Error:", str(e))
        return JsonResponse({'error': 'Failed to initiate payment'}, status=500)

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            print("M-Pesa Callback received:", json.dumps(body, indent=2))

            result_code = body.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            result_desc = body.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
            checkout_request_id = body.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')

            if result_code == 0:
                # Transaction successful
                metadata = body['Body']['stkCallback'].get('CallbackMetadata', {}).get('Item', [])
                transaction_data = {item['Name']: item.get('Value') for item in metadata}
                print("Transaction Metadata:", json.dumps(transaction_data, indent=2))

                # You could save transaction_data into your DB here

                return JsonResponse({'message': 'Payment successful', 'data': transaction_data})
            else:
                print("Transaction Failed:", result_desc)
                return JsonResponse({'message': 'Payment failed', 'description': result_desc})

        except Exception as e:
            print("Callback Error:", str(e))
            return JsonResponse({'error': 'Invalid callback data'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def process_payment(request):
    return JsonResponse({'message': 'Process payment placeholder'})

@csrf_exempt
def create_payment(request):
    return JsonResponse({'message': 'Stripe simulation placeholder'})