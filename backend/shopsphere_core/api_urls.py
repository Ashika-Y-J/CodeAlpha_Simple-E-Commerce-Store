from django.urls import path
from store.api_views import (
    CategoryListAPIView, ProductListAPIView,
    ProductDetailAPIView, ProductReviewCreateAPIView
)
from cart.api_views import (
    CartAPIView, CartAddAPIView, CartUpdateAPIView,
    CartRemoveAPIView, CartClearAPIView
)
from orders.api_views import (
    OrderCheckoutAPIView, OrderDetailAPIView, OrderHistoryAPIView
)
from accounts.api_views import (
    AuthRegisterAPIView, AuthLoginAPIView,
    AuthLogoutAPIView, AuthProfileAPIView
)

urlpatterns = [
    # Store & Products
    path('categories/', CategoryListAPIView.as_view(), name='api_categories'),
    path('products/', ProductListAPIView.as_view(), name='api_products'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('products/<slug:slug>/reviews/', ProductReviewCreateAPIView.as_view(), name='api_product_review'),

    # Cart
    path('cart/', CartAPIView.as_view(), name='api_cart'),
    path('cart/add/', CartAddAPIView.as_view(), name='api_cart_add'),
    path('cart/update/', CartUpdateAPIView.as_view(), name='api_cart_update'),
    path('cart/remove/', CartRemoveAPIView.as_view(), name='api_cart_remove'),
    path('cart/clear/', CartClearAPIView.as_view(), name='api_cart_clear'),

    # Orders
    path('orders/checkout/', OrderCheckoutAPIView.as_view(), name='api_checkout'),
    path('orders/history/', OrderHistoryAPIView.as_view(), name='api_order_history'),
    path('orders/<str:order_number>/', OrderDetailAPIView.as_view(), name='api_order_detail'),

    # Auth
    path('auth/register/', AuthRegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', AuthLoginAPIView.as_view(), name='api_login'),
    path('auth/logout/', AuthLogoutAPIView.as_view(), name='api_logout'),
    path('auth/profile/', AuthProfileAPIView.as_view(), name='api_profile'),
]

