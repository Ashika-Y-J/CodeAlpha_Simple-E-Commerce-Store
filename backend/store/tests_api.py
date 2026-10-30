from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product
from decimal import Decimal

class ApiEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Tech', slug='tech', icon='fa-laptop')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Tech Gadget',
            slug='test-tech-gadget',
            price=Decimal('120.00'),
            stock=15,
            is_available=True,
            is_featured=True
        )

    def test_api_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]['slug'], 'tech')

    def test_api_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['count'] >= 1)
        self.assertEqual(data['results'][0]['slug'], 'test-tech-gadget')

    def test_api_product_detail(self):
        response = self.client.get('/api/products/test-tech-gadget/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['product']['name'], 'Test Tech Gadget')

    def test_api_cart_flow(self):
        # Add to cart
        add_res = self.client.post('/api/cart/add/', {'product_id': self.product.id, 'quantity': 2}, content_type='application/json')
        self.assertEqual(add_res.status_code, 200)
        data = add_res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart']['count'], 2)

        # Get cart
        get_res = self.client.get('/api/cart/')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()['count'], 2)

        # Update cart
        update_res = self.client.post('/api/cart/update/', {'product_id': self.product.id, 'action': 'decrease'}, content_type='application/json')
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.json()['cart']['count'], 1)

    def test_api_checkout_flow(self):
        # Place order via API
        order_payload = {
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'email': 'sarah@test.com',
            'phone': '1234567890',
            'address_line1': '101 Cyberdyne Way',
            'city': 'Los Angeles',
            'state': 'CA',
            'postal_code': '90001',
            'payment_method': 'card',
            'cart_items': [
                {'product_id': self.product.id, 'quantity': 1}
            ]
        }
        res = self.client.post('/api/orders/checkout/', order_payload, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res_data = res.json()
        self.assertTrue(res_data['success'])
        self.assertIn('order_number', res_data)

        # Fetch order details
        order_num = res_data['order_number']
        detail_res = self.client.get(f'/api/orders/{order_num}/')
        self.assertEqual(detail_res.status_code, 200)
        self.assertEqual(detail_res.json()['first_name'], 'Sarah')

