from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product
from orders.models import Order
from decimal import Decimal

class OrdersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testbuyer', password='password123', email='buyer@test.com')
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.product = Product.objects.create(
            category=self.category,
            name='Bluetooth Speaker',
            slug='bluetooth-speaker',
            price=Decimal('60.00'),
            stock=10,
            is_available=True
        )

    def test_checkout_empty_cart_redirect(self):
        # Empty cart should redirect to product list
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 302)

    def test_complete_checkout_process(self):
        # Add item to cart
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})

        # Submit checkout
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'phone': '+1 (555) 123-4567',
            'address_line1': '456 Elm Street',
            'address_line2': 'Suite 101',
            'city': 'Seattle',
            'state': 'WA',
            'postal_code': '98101',
            'country': 'United States',
            'payment_method': 'cod',
            'order_notes': 'Please leave near the front door.'
        }
        response = self.client.post(reverse('orders:checkout'), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify order in database
        order = Order.objects.filter(email='jane.doe@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product_name, 'Bluetooth Speaker')
        self.assertEqual(order.subtotal, Decimal('60.00'))

        # Verify confirmation page contains order number
        self.assertContains(response, order.order_number)
        self.assertContains(response, 'Thank You for Your Order')
