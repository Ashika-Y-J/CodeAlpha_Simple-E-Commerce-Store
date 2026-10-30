from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_image', 'price', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'subtotal', 'shipping_cost',
            'tax_amount', 'total_amount', 'payment_method', 'payment_method_display',
            'payment_status', 'order_status', 'order_notes', 'items', 'created_at'
        ]

