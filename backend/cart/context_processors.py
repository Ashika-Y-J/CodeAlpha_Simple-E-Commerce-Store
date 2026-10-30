from .cart import Cart

def cart(request):
    """Context processor that makes the cart accessible to all templates."""
    cart_obj = Cart(request)
    return {
        'cart': cart_obj,
        'cart_count': len(cart_obj),
        'cart_subtotal': cart_obj.get_subtotal(),
    }

