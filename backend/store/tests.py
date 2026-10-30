from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product, Review
from django.contrib.auth.models import User
from decimal import Decimal

class StoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Wireless Headphones',
            slug='test-wireless-headphones',
            price=Decimal('99.99'),
            stock=10,
            is_available=True,
            is_featured=True
        )
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_home_view(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ShopSphere')
        self.assertContains(response, 'Test Wireless Headphones')

    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')

    def test_product_list_by_category(self):
        response = self.client.get(reverse('store:product_list_by_category', args=['electronics']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electronics')

    def test_product_search(self):
        response = self.client.get(reverse('store:product_list') + '?q=Headphones')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', args=['test-wireless-headphones']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')
        self.assertContains(response, '$99.99')

    def test_submit_review(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('store:product_detail', args=['test-wireless-headphones']), {
            'rating': 5,
            'title': 'Great sound',
            'comment': 'Love the bass and comfort!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())
