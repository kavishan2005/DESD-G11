from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from .models import Cart, CartItem, Order, OrderItem, SubOrder, RecurringOrder, RecurringOrderItem
from products.models import Product, Producer

def get_or_create_cart(request):
    """Get or create a cart for the current user"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        return cart
    return None

@login_required
def cart_view(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'orders/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Added {product.name} to cart.')
    return redirect('orders:cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    
    return redirect('orders:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('orders:cart')

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    
    if not cart or cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('products:product_list')
    
    items_by_producer = {}
    for item in cart.items.all():
        producer = item.product.producer
        if producer not in items_by_producer:
            items_by_producer[producer] = []
        items_by_producer[producer].append(item)
    
    is_multi = len(items_by_producer) > 1
    
    if request.method == 'POST':
        delivery_date = request.POST.get('delivery_date')
        delivery_address = request.POST.get('delivery_address')
        instructions = request.POST.get('instructions', '')
        
        min_date = timezone.now().date() + timedelta(days=2)
        selected_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
        
        if selected_date < min_date:
            messages.error(request, "Delivery must be at least 48 hours from now.")
            return redirect('orders:checkout')
        
        order = Order.objects.create(
            customer=request.user,
            delivery_address=delivery_address,
            delivery_date=selected_date,
            delivery_instructions=instructions,
            status='pending'
        )
        
        subtotal = 0
        
        if is_multi:
            for producer, items in items_by_producer.items():
                producer_subtotal = sum(item.subtotal for item in items)
                producer_commission = producer_subtotal * Decimal('0.05')
                
                SubOrder.objects.create(
                    order=order,
                    producer=producer,
                    status='pending',
                    subtotal=producer_subtotal,
                    commission=producer_commission,
                    producer_payment=producer_subtotal - producer_commission,
                    delivery_date=selected_date
                )
                
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        producer=producer,
                        quantity=item.quantity,
                        unit_price=item.product.price
                    )
                    subtotal += item.subtotal
        else:
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    producer=item.product.producer,
                    quantity=item.quantity,
                    unit_price=item.product.price
                )
                subtotal += item.subtotal
        
        order.subtotal = subtotal
        order.commission = subtotal * Decimal('0.05')
        order.total = subtotal - order.commission
        order.save()
        
        cart.items.all().delete()
        
        messages.success(request, f"Order placed! Order number: {order.order_number}")
        return redirect('orders:order_detail', order_id=order.id)
    
    min_delivery = (timezone.now() + timedelta(days=2)).date()
    
    context = {
        'cart': cart,
        'items_by_producer': items_by_producer,
        'total': cart.total,
        'min_delivery': min_delivery,
        'is_multi': is_multi,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    """Display all orders for the logged-in customer"""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    print(f"ORDER HISTORY: User {request.user.username} has {orders.count()} orders")
    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def producer_orders(request):
    try:
        producer = request.user.producer
    except:
        messages.error(request, "You need a producer account.")
        return redirect('home')
    
    suborders = SubOrder.objects.filter(producer=producer).order_by('-delivery_date')
    return render(request, 'orders/producer_orders.html', {'suborders': suborders})

@login_required
def update_order_status(request, suborder_id):
    suborder = get_object_or_404(SubOrder, id=suborder_id, producer=request.user.producer)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            suborder.status = new_status
            suborder.save()
            messages.success(request, f"Order status updated to {new_status}")
    
    return redirect('orders:producer_orders')

# ========== SPRINT 3 FEATURES ==========

@login_required
def recurring_orders(request):
    """View and manage recurring orders"""
    recurring_orders = RecurringOrder.objects.filter(customer=request.user, is_active=True)
    return render(request, 'orders/recurring_orders.html', {'recurring_orders': recurring_orders})

@login_required
def create_recurring_order(request):
    """Create a new recurring order from current cart"""
    cart = get_or_create_cart(request)
    
    if not cart or cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('products:product_list')
    
    if request.method == 'POST':
        name = request.POST.get('name', 'My Weekly Order')
        frequency = request.POST.get('frequency', 'weekly')
        delivery_date = request.POST.get('next_delivery_date')
        next_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
        
        recurring = RecurringOrder.objects.create(
            customer=request.user,
            name=name,
            frequency=frequency,
            next_delivery_date=next_date,
            delivery_instructions=request.POST.get('instructions', '')
        )
        
        for item in cart.items.all():
            RecurringOrderItem.objects.create(
                recurring_order=recurring,
                product=item.product,
                quantity=item.quantity
            )
        
        messages.success(request, f"Recurring order '{name}' created!")
        return redirect('orders:recurring_orders')
    
    min_date = timezone.now().date() + timedelta(days=7)
    context = {'cart': cart, 'min_date': min_date}
    return render(request, 'orders/create_recurring.html', context)

@login_required
def cancel_recurring_order(request, recurring_id):
    """Cancel a recurring order"""
    recurring = get_object_or_404(RecurringOrder, id=recurring_id, customer=request.user)
    recurring.is_active = False
    recurring.save()
    messages.success(request, f"Recurring order '{recurring.name}' cancelled.")
    return redirect('orders:recurring_orders')

@login_required
def bulk_order(request):
    """Bulk ordering for community groups"""
    if request.user.profile.user_type != 'community':
        messages.error(request, "This feature is for community groups only")
        return redirect('products:product_list')
    
    cart = get_or_create_cart(request)
    
    if not cart or cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('products:product_list')
    
    if request.method == 'POST':
        delivery_date = request.POST.get('delivery_date')
        delivery_address = request.POST.get('delivery_address')
        instructions = request.POST.get('instructions', '')
        
        min_date = timezone.now().date() + timedelta(days=2)
        selected_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
        
        if selected_date < min_date:
            messages.error(request, "Delivery must be at least 48 hours from now.")
            return redirect('orders:bulk_order')
        
        items_by_producer = {}
        for item in cart.items.all():
            producer = item.product.producer
            if producer not in items_by_producer:
                items_by_producer[producer] = []
            items_by_producer[producer].append(item)
        
        order = Order.objects.create(
            customer=request.user,
            delivery_address=delivery_address,
            delivery_date=selected_date,
            delivery_instructions=instructions,
            status='pending'
        )
        
        subtotal = 0
        for producer, items in items_by_producer.items():
            producer_subtotal = sum(item.subtotal for item in items)
            producer_commission = producer_subtotal * Decimal('0.05')
            
            SubOrder.objects.create(
                order=order,
                producer=producer,
                status='pending',
                subtotal=producer_subtotal,
                commission=producer_commission,
                producer_payment=producer_subtotal - producer_commission,
                delivery_date=selected_date
            )
            
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    producer=producer,
                    quantity=item.quantity,
                    unit_price=item.product.price
                )
                subtotal += item.subtotal
        
        order.subtotal = subtotal
        order.commission = subtotal * Decimal('0.05')
        order.total = subtotal - order.commission
        order.save()
        
        cart.items.all().delete()
        
        messages.success(request, f"Bulk order placed! Order number: {order.order_number}")
        return redirect('orders:order_detail', order_id=order.id)
    
    min_delivery = (timezone.now() + timedelta(days=2)).date()
    context = {'cart': cart, 'min_delivery': min_delivery}
    return render(request, 'orders/bulk_order.html', context)

def send_notification(user, notification_type, title, message, link=''):
    """Helper function to create notifications"""
    from notifications.models import Notification
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )