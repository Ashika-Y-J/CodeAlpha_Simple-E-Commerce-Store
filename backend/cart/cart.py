from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the cart from Django session."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # Ensure minimum quantity of 1 and maximum of stock or 99
        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product)
        else:
            if product.stock and self.cart[product_id]['quantity'] > product.stock:
                self.cart[product_id]['quantity'] = product.stock
            self.save()

    def update_quantity(self, product, quantity):
        """Set exact quantity for a product."""
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity > 0:
                if product.stock and quantity > product.stock:
                    quantity = product.stock
                self.cart[product_id]['quantity'] = quantity
                self.save()
            else:
                self.remove(product)

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """Mark session as modified to ensure it gets saved."""
        self.session.modified = True

    def clear(self):
        """Empty the cart session."""
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and fetch products from DB without mutating session."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        for pid, item in self.cart.items():
            if pid in product_map:
                price = Decimal(str(item['price']))
                qty = int(item['quantity'])
                yield {
                    'product': product_map[pid],
                    'quantity': qty,
                    'price': price,
                    'total_price': price * qty,
                }

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        """Calculate total price of all items."""
        return sum(Decimal(str(item['price'])) * item['quantity'] for item in self.cart.values())

    def get_shipping_fee(self):
        """Free shipping on orders >= $50, else $9.99 (0 if empty)."""
        subtotal = self.get_subtotal()
        if subtotal == Decimal('0.00') or len(self) == 0:
            return Decimal('0.00')
        if subtotal >= Decimal('50.00'):
            return Decimal('0.00')
        return Decimal('9.99')

    def get_tax(self):
        """Estimate 5% tax."""
        subtotal = self.get_subtotal()
        if subtotal == Decimal('0.00') or len(self) == 0:
            return Decimal('0.00')
        return round(subtotal * Decimal('0.05'), 2)

    def get_total(self):
        """Calculate final grand total."""
        if len(self) == 0:
            return Decimal('0.00')
        return self.get_subtotal() + self.get_shipping_fee() + self.get_tax()
