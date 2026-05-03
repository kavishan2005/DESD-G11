from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from orders.models import Order

@login_required
def create_payment_intent(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return JsonResponse({'clientSecret': 'test_client_secret'})

@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payments/payment.html', {'order': order})

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.payment_status = 'succeeded'
    order.status = 'confirmed'
    order.save()
    messages.success(request, f'Payment successful! Order #{order.order_number} confirmed.')
    return redirect('orders:order_detail', order_id=order.id)

@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.payment_status = 'cancelled'
    order.status = 'cancelled'
    order.save()
    messages.warning(request, 'Payment was cancelled.')
    return redirect('orders:cart')
