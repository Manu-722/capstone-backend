from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Shoe, CartItem, Order
from users.models import Profile  
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

#  Public landing
def landing(request):
    return HttpResponse("Welcome to Cyman Wears API!")

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
        'category': shoe.category,
        'section': shoe.section, 
        'sizes': shoe.sizes,
    } for shoe in shoes]
    return Response(data)

#  Get cart items (model-based flow)
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
        'discounted': float(item.discounted_price()),
        'total': float(item.total_price()),
    } for item in cart_items]
    return Response(data)

#  Add to cart
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

# Place an order
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

#  Persistent cart via user profile (JSONField)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return Response({'items': profile.cart_data or []})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def persist_user_cart(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.cart_data = request.data
    profile.save()
    return Response({'message': 'Cart saved successfully'})

#  Wishlist views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return Response({'items': profile.wishlist or []})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    item = request.data
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.wishlist.append(item)
    profile.save()
    return Response({'message': 'Added to wishlist'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, item_id):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.wishlist = [i for i in profile.wishlist if i.get('id') != item_id]
    profile.save()
    return Response({'message': 'Removed from wishlist'})