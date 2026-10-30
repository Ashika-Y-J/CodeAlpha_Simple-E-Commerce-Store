from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from decimal import Decimal
from cart.cart import Cart
from store.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderCheckoutAPIView(APIView):
    """API endpoint to process checkout and place an order."""
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        cart = Cart(request)

        # Check if cart items passed explicitly in body (useful for stateless REST clients / localStorage cart)
        custom_items = data.get('cart_items')
        
        items_to_process = []
        if custom_items and len(custom_items) > 0:
            subtotal = Decimal('0.00')
            for c_item in custom_items:
                try:
                    product = Product.objects.get(id=c_item['product_id'])
                    qty = int(c_item.get('quantity', 1))
                    item_total = product.price * qty
                    subtotal += item_total
                    items_to_process.append({
                        'product': product,
                        'price': product.price,
                        'quantity': qty,
                        'total_price': item_total
                    })
                except Product.DoesNotExist:
                    continue
            shipping = Decimal('0.00') if subtotal >= Decimal('50.00') else Decimal('9.99')
            tax = round(subtotal * Decimal('0.05'), 2)
            total = subtotal + shipping + tax
        else:
            if len(cart) == 0:
                return Response({'error': 'Shopping cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            subtotal = cart.get_subtotal()
            shipping = cart.get_shipping_fee()
            tax = cart.get_tax()
            total = cart.get_total()
            for item in cart:
                items_to_process.append(item)

        # Validate required shipping fields
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        address_line1 = data.get('address_line1', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()
        postal_code = data.get('postal_code', '').strip()
        country = data.get('country', 'United States').strip()
        payment_method = data.get('payment_method', 'cod')
        order_notes = data.get('order_notes', '').strip()

        if not all([first_name, last_name, email, phone, address_line1, city, state, postal_code]):
            return Response({'error': 'Please fill all required shipping fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Payment status simulation
        payment_status = 'Paid' if payment_method in ['card', 'upi'] else 'Pending'

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_line1=address_line1,
            address_line2=data.get('address_line2', ''),
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            subtotal=subtotal,
            shipping_cost=shipping,
            tax_amount=tax,
            total_amount=total,
            payment_method=payment_method,
            payment_status=payment_status,
            order_status='Confirmed',
            order_notes=order_notes
        )

        for it in items_to_process:
            prod = it['product']
            OrderItem.objects.create(
                order=order,
                product=prod,
                product_name=prod.name,
                product_image=prod.display_image,
                price=it['price'],
                quantity=it['quantity'],
                total_price=it['total_price']
            )
            # Update stock
            if prod.stock >= it['quantity']:
                prod.stock -= it['quantity']
                if prod.stock == 0:
                    prod.is_available = False
                prod.save()

        # Clear session cart if used
        if len(cart) > 0:
            cart.clear()

        return Response({
            'success': True,
            'message': 'Order placed successfully!',
            'order_number': order.order_number,
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    """API endpoint to get order details by order_number."""
    permission_classes = [AllowAny]

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderHistoryAPIView(APIView):
    """API endpoint to get order history for authenticated user."""
    def get(self, request):
        if not request.user.is_authenticated:
            # Fallback for demo: return orders matching customer email or recent orders
            orders = Order.objects.all().order_by('-created_at')[:5]
        else:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

