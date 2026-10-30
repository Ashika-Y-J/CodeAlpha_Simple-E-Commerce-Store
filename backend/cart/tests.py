from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product
from decimal import Decimal

class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            category=self.category,
            name='Smart Watch',
            slug='smart-watch',
            price=Decimal('50.00'),
            stock=5,
            is_available=True
        )

    def test_cart_empty_detail(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Cart is Empty')

    def test_cart_add_and_view(self):
        # Add item to cart
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), {
            'quantity': 2
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Check cart detail page
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, 'Smart Watch')
        self.assertContains(response, '100.00')

    def test_cart_ajax_add(self):
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 1)

    def test_cart_update(self):
        # Add 1 item
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        # Increase quantity
        response = self.client.post(
            reverse('cart:cart_update', args=[self.product.id]),
            {'action': 'increase'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['item_quantity'], 2)

    def test_cart_remove(self):
        # Add item then remove
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Cart is Empty')
