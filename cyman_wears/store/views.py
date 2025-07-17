from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Shoe, CartItem, Order
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

def landing(request):
    return HttpResponse("Welcome to Cyman Wears API!")

# def get_shoes(request):
#     shoes = Shoe.objects.all().values()
#     return JsonResponse(list(shoes), safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    data = [{
        'id': item.id,
        'shoe': item.shoe.name,
        'image': str(item.shoe.image),
        'description': item.shoe.description,
        'quantity': item.quantity,
        'price': float(item.shoe.price),
        'discounted': float(item.discounted_price()),  # Include discount logic
        'total': float(item.total_price()),
    } for item in cart_items]
    return Response(data)
@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        shoe_id = data.get('shoe_id')
        quantity = data.get('quantity', 1)
        item, created = CartItem.objects.get_or_create(user=request.user, shoe_id=shoe_id)
        if not created:
            item.quantity += quantity
        item.save()
        return JsonResponse({'message': 'Item added to cart'})

@csrf_exempt
@login_required
def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address = data.get('address')
        payment_method = data.get('payment_method')

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        total = sum(item.discounted_price() for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            total=total,
            address=address,
            payment_method=payment_method,
            paid=(payment_method == 'mpesa'),
            status='Pending'
        )
        order.items.set(cart_items)
        order.save()

        return JsonResponse({'message': 'Order placed', 'order_id': order.id})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_shoes(request):
    shoes = Shoe.objects.all().order_by('-created_at')
    data = [{
        'id': shoe.id,
        'name': shoe.name,
        'price': float(shoe.price),
        'image': str(shoe.image),
        'description': shoe.description,
        'in_stock': shoe.in_stock,
        'created_at': shoe.created_at.isoformat(),
    } for shoe in shoes]
    return Response(data)
