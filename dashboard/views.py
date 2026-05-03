from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from accounts.models import Profile
from orders.models import Order, SubOrder
from products.models import Product, Producer

@staff_member_required
def admin_dashboard(request):
    """Custom admin dashboard - only accessible by staff/admin users"""
    
    # Statistics
    total_users = User.objects.count()
    total_producers = Profile.objects.filter(user_type='producer').count()
    total_customers = Profile.objects.filter(user_type='customer').count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_revenue = Order.objects.aggregate(total=Sum('total'))['total'] or 0
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Low stock alerts
    low_stock_products = Product.objects.filter(stock_quantity__lt=10)[:5]
    
    context = {
        'total_users': total_users,
        'total_producers': total_producers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
