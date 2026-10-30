from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from store.models import Product
from .cart import Cart

def cart_detail(request):
    """View shopping cart page."""
    cart = Cart(request)
    subtotal = cart.get_subtotal()
    shipping = cart.get_shipping_fee()
    tax = cart.get_tax()
    total = cart.get_total()

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request, product_id):
    """Add product to cart via POST or AJAX."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = 1
    if 'quantity' in request.POST:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

    cart.add(product=product, quantity=quantity)

    # Check if this was an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" added to cart!',
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_subtotal()),
            'product_name': product.name,
        })

    messages.success(request, f'"{product.name}" was added to your shopping cart.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart:cart_detail'
    return redirect(next_url)


@require_POST
def cart_update(request, product_id):
    """Update item quantity in cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    quantity = request.POST.get('quantity')

    current_qty = cart.cart.get(str(product.id), {}).get('quantity', 1)

    if action == 'increase':
        cart.add(product=product, quantity=1)
    elif action == 'decrease':
        if current_qty > 1:
            cart.add(product=product, quantity=-1)
        else:
            cart.remove(product)
    elif quantity is not None:
        try:
            qty_val = int(quantity)
            if qty_val > 0:
                cart.update_quantity(product=product, quantity=qty_val)
            else:
                cart.remove(product)
        except ValueError:
            pass

    # Check AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_qty = cart.cart.get(str(product.id), {}).get('quantity', 0)
        item_total = str(product.price * item_qty) if item_qty > 0 else '0.00'
        return JsonResponse({
            'success': True,
            'item_quantity': item_qty,
            'item_total': item_total,
            'cart_count': len(cart),
            'subtotal': str(cart.get_subtotal()),
            'shipping': str(cart.get_shipping_fee()),
            'tax': str(cart.get_tax()),
            'total': str(cart.get_total()),
        })

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove product completely from cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" removed from cart',
            'cart_count': len(cart),
            'subtotal': str(cart.get_subtotal()),
            'shipping': str(cart.get_shipping_fee()),
            'tax': str(cart.get_tax()),
            'total': str(cart.get_total()),
        })

    messages.info(request, f'"{product.name}" was removed from your cart.')
    return redirect('cart:cart_detail')


def cart_clear(request):
    """Clear all items from cart."""
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Your shopping cart has been emptied.')
    return redirect('cart:cart_detail')
