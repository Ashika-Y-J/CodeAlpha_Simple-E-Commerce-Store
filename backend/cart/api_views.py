from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from store.models import Product
from .cart import Cart

def format_cart_data(cart):
    items = []
    for item in cart:
        product = item['product']
        items.append({
            'product_id': product.id,
            'name': product.name,
            'slug': product.slug,
            'category_name': product.category.name,
            'price': str(item['price']),
            'quantity': item['quantity'],
            'total_price': str(item['total_price']),
            'image': product.display_image,
            'stock': product.stock,
        })
    return {
        'items': items,
        'count': len(cart),
        'subtotal': str(cart.get_subtotal()),
        'shipping': str(cart.get_shipping_fee()),
        'tax': str(cart.get_tax()),
        'total': str(cart.get_total()),
    }

class CartAPIView(APIView):
    """API endpoint to get the current shopping cart state."""
    permission_classes = [AllowAny]

    def get(self, request):
        cart = Cart(request)
        return Response(format_cart_data(cart))


class CartAddAPIView(APIView):
    """API endpoint to add a product to the cart."""
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=quantity)

        cart_data = format_cart_data(cart)
        return Response({
            'success': True,
            'message': f'"{product.name}" added to cart!',
            'cart': cart_data
        })


class CartUpdateAPIView(APIView):
    """API endpoint to increase, decrease, or set product quantity."""
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get('product_id')
        action = request.data.get('action') # 'increase', 'decrease', or 'set'
        quantity = request.data.get('quantity')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)

        if action == 'increase':
            cart.add(product=product, quantity=1)
        elif action == 'decrease':
            cart.add(product=product, quantity=-1)
        elif quantity is not None:
            try:
                cart.update_quantity(product=product, quantity=int(quantity))
            except ValueError:
                pass

        return Response({
            'success': True,
            'cart': format_cart_data(cart)
        })


class CartRemoveAPIView(APIView):
    """API endpoint to remove an item completely from cart."""
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)

        return Response({
            'success': True,
            'message': f'"{product.name}" removed from cart',
            'cart': format_cart_data(cart)
        })


class CartClearAPIView(APIView):
    """API endpoint to clear all items from the cart."""
    permission_classes = [AllowAny]

    def post(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({
            'success': True,
            'message': 'Shopping cart cleared',
            'cart': format_cart_data(cart)
        })

