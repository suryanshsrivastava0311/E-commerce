import stripe
import uuid
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItems
from cart.views import _cart_id
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request):

    subtotal = 0
    tax = 0
    total = 0

#  get cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
    except Cart.DoesNotExist:
        return redirect('cart')

# calculate subtotal
    for cart_item in cart_items:
        subtotal += cart_item.product.price * cart_item.quantity

    if subtotal <= 0:
        return redirect('cart')
    
    tax = (2 * subtotal) / 100
    total = subtotal + tax

    total_amount_paise = int(total * 100)

    # create order
    order = Order.objects.create(
        user=request.user,
        order_number=str(uuid.uuid4()),
        subtotal=subtotal,
        tax=tax,
        total_amount=total
    )

# Stripe Checkout 
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': f'Order {order.order_number}',
                },
                'unit_amount': total_amount_paise,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/payments/success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/payments/cancel/',
        metadata={
            'order_id': order.id
        }
    )

    return redirect(session.url)


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return redirect('cart')

    session = stripe.checkout.Session.retrieve(session_id)

    order_id = session.metadata.get('order_id')
    order = Order.objects.get(id=order_id)

    order.is_paid = True
    order.stripe_payment_id = session.payment_intent
    order.save()
# clear cart
    cart = Cart.objects.get(cart_id=_cart_id(request))
    CartItems.objects.filter(cart=cart).delete()

    return render(request, 'payments/success.html', {'order': order})

# cancel payment
def payment_cancel(request):
    return render(request, 'payments/cancel.html')
