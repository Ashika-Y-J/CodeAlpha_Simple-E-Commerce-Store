from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm

def checkout(request):
    """Checkout page to collect shipping address and payment method."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your shopping cart is currently empty. Please add items before checkout.')
        return redirect('store:product_list')

    # Pre-populate form data for authenticated user
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data.update({
                'phone': profile.phone,
                'address_line1': profile.address,
                'city': profile.city,
                'state': profile.state,
                'postal_code': profile.postal_code,
                'country': profile.country,
            })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            order.subtotal = cart.get_subtotal()
            order.shipping_cost = cart.get_shipping_fee()
            order.tax_amount = cart.get_tax()
            order.total_amount = cart.get_total()
            
            # Payment simulation
            if order.payment_method in ['card', 'upi']:
                order.payment_status = 'Paid'
            else:
                order.payment_status = 'Pending'
                
            order.order_status = 'Confirmed'
            order.save()

            # Create Order Items and decrease product stock
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_image=product.display_image,
                    price=item['price'],
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )
                if product.stock >= item['quantity']:
                    product.stock -= item['quantity']
                    if product.stock == 0:
                        product.is_available = False
                    product.save()

            # Clear cart
            cart.clear()

            messages.success(request, f'Congratulations! Your order #{order.order_number} has been placed successfully.')
            return redirect('orders:order_confirmation', order_number=order.order_number)
        else:
            messages.error(request, 'Please check the checkout form for errors.')
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'subtotal': cart.get_subtotal(),
        'shipping': cart.get_shipping_fee(),
        'tax': cart.get_tax(),
        'total': cart.get_total(),
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_number):
    """Order confirmation and receipt page."""
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_confirmation.html', context)


@login_required
def order_history(request):
    """List of orders placed by the logged-in customer."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail(request, order_number):
    """Single order detail view for customer."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)
