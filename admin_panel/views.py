from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from accounts.models import Profile
from orders.models import Order
from products.models import Product, Producer

@staff_member_required
def admin_dashboard(request):
    """Custom admin dashboard with real statistics"""
    
    # User Statistics
    total_users = User.objects.count()
    total_producers = Profile.objects.filter(user_type='producer').count()
    total_customers = Profile.objects.filter(user_type='customer').count()
    
    # Order Statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='delivered').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    
    # Revenue
    total_revenue = Order.objects.aggregate(total=Sum('total'))['total'] or 0
    total_commission = Order.objects.aggregate(total=Sum('commission'))['total'] or 0
    
    # Recent Orders (last 10)
    recent_orders = Order.objects.order_by('-created_at')[:10]
    
    # Low Stock Products (less than 10 items)
    low_stock = Product.objects.filter(stock_quantity__lt=10)[:10]
    
    # Recent Users (last 10)
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Product Statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(availability_status='available').count()
    
    # Producer Statistics
    total_producers_count = Producer.objects.count()
    active_producers = Producer.objects.filter(is_active=True).count()
    
    context = {
        # User stats
        'total_users': total_users,
        'total_producers': total_producers,
        'total_customers': total_customers,
        
        # Order stats
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        
        # Revenue stats
        'total_revenue': total_revenue,
        'total_commission': total_commission,
        
        # Product stats
        'total_products': total_products,
        'active_products': active_products,
        'low_stock': low_stock,
        
        # Producer stats
        'total_producers_count': total_producers_count,
        'active_producers': active_producers,
        
        # Recent data
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    }
    return render(request, 'admin_panel/dashboard.html', context)
@staff_member_required
def commission_report(request):
    """Generate commission report"""
    from orders.models import Order
    from django.db.models import Sum
    from datetime import datetime, timedelta
    
    # Get date range from request
    days = int(request.GET.get('range', 30))
    start_date = datetime.now() - timedelta(days=days)
    
    orders = Order.objects.filter(created_at__gte=start_date)
    
    context = {
        'total_orders': orders.count(),
        'total_revenue': orders.aggregate(total=Sum('total'))['total'] or 0,
        'total_commission': orders.aggregate(total=Sum('commission'))['total'] or 0,
        'recent_orders': orders.order_by('-created_at')[:20],
        'date_range': days,
    }
    return render(request, 'admin_panel/commission_report.html', context)
@staff_member_required
def commission_report(request):
    """Generate commission report for admin"""
    from orders.models import Order
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    from calendar import month_name
    
    # Get date range
    range_days = request.GET.get('range', '30')
    try:
        days = int(range_days)
    except:
        days = 30
    
    start_date = datetime.now() - timedelta(days=days)
    orders = Order.objects.filter(created_at__gte=start_date)
    
    # Monthly summary
    monthly_summary = []
    for i in range(1, 13):
        month_orders = orders.filter(created_at__month=i)
        if month_orders.exists():
            monthly_summary.append({
                'month': month_name[i],
                'count': month_orders.count(),
                'revenue': month_orders.aggregate(total=Sum('total'))['total'] or 0,
                'commission': month_orders.aggregate(total=Sum('commission'))['total'] or 0,
            })
    
    context = {
        'total_orders': orders.count(),
        'total_revenue': orders.aggregate(total=Sum('total'))['total'] or 0,
        'total_commission': orders.aggregate(total=Sum('commission'))['total'] or 0,
        'avg_order_value': (orders.aggregate(total=Sum('total'))['total'] or 0) / max(orders.count(), 1),
        'recent_orders': orders.order_by('-created_at')[:20],
        'monthly_summary': monthly_summary,
        'date_range': days,
    }
    return render(request, 'admin_panel/commission_report.html', context)

@staff_member_required
def commission_report(request):
    """Generate commission report for admin"""
    from orders.models import Order
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    from calendar import month_name
    
    # Get date range
    range_days = request.GET.get('range', '30')
    try:
        days = int(range_days)
    except:
        days = 30
    
    start_date = datetime.now() - timedelta(days=days)
    orders = Order.objects.filter(created_at__gte=start_date)
    
    # Monthly summary
    monthly_summary = []
    for i in range(1, 13):
        month_orders = orders.filter(created_at__month=i)
        if month_orders.exists():
            monthly_summary.append({
                'month': month_name[i],
                'count': month_orders.count(),
                'revenue': month_orders.aggregate(total=Sum('total'))['total'] or 0,
                'commission': month_orders.aggregate(total=Sum('commission'))['total'] or 0,
            })
    
    context = {
        'total_orders': orders.count(),
        'total_revenue': orders.aggregate(total=Sum('total'))['total'] or 0,
        'total_commission': orders.aggregate(total=Sum('commission'))['total'] or 0,
        'avg_order_value': (orders.aggregate(total=Sum('total'))['total'] or 0) / max(orders.count(), 1),
        'recent_orders': orders.order_by('-created_at')[:20],
        'monthly_summary': monthly_summary,
        'date_range': days,
    }
    return render(request, 'admin_panel/commission_report.html', context)

@staff_member_required
def commission_report(request):
    """Generate commission report for admin"""
    from orders.models import Order
    from django.db.models import Sum
    from datetime import datetime, timedelta
    from calendar import month_name
    
    # Get date range
    range_days = request.GET.get('range', '30')
    try:
        days = int(range_days)
    except:
        days = 30
    
    start_date = datetime.now() - timedelta(days=days)
    orders = Order.objects.filter(created_at__gte=start_date)
    
    # Monthly summary
    monthly_summary = []
    for i in range(1, 13):
        month_orders = orders.filter(created_at__month=i)
        if month_orders.exists():
            monthly_summary.append({
                'month': month_name[i],
                'count': month_orders.count(),
                'revenue': month_orders.aggregate(total=Sum('total'))['total'] or 0,
                'commission': month_orders.aggregate(total=Sum('commission'))['total'] or 0,
            })
    
    context = {
        'total_orders': orders.count(),
        'total_revenue': orders.aggregate(total=Sum('total'))['total'] or 0,
        'total_commission': orders.aggregate(total=Sum('commission'))['total'] or 0,
        'avg_order_value': (orders.aggregate(total=Sum('total'))['total'] or 0) / max(orders.count(), 1),
        'recent_orders': orders.order_by('-created_at')[:20],
        'monthly_summary': monthly_summary,
        'date_range': days,
    }
    return render(request, 'admin_panel/commission_report.html', context)

@staff_member_required
def commission_report(request):
    """Generate commission report for admin"""
    from orders.models import Order
    from django.db.models import Sum
    from datetime import datetime, timedelta
    from calendar import month_name
    
    range_days = request.GET.get('range', '30')
    try:
        days = int(range_days)
    except:
        days = 30
    
    start_date = datetime.now() - timedelta(days=days)
    orders = Order.objects.filter(created_at__gte=start_date)
    
    monthly_summary = []
    for i in range(1, 13):
        month_orders = orders.filter(created_at__month=i)
        if month_orders.exists():
            monthly_summary.append({
                'month': month_name[i],
                'count': month_orders.count(),
                'revenue': month_orders.aggregate(total=Sum('total'))['total'] or 0,
                'commission': month_orders.aggregate(total=Sum('commission'))['total'] or 0,
            })
    
    context = {
        'total_orders': orders.count(),
        'total_revenue': orders.aggregate(total=Sum('total'))['total'] or 0,
        'total_commission': orders.aggregate(total=Sum('commission'))['total'] or 0,
        'avg_order_value': (orders.aggregate(total=Sum('total'))['total'] or 0) / max(orders.count(), 1),
        'recent_orders': orders.order_by('-created_at')[:20],
        'monthly_summary': monthly_summary,
        'date_range': days,
    }
    return render(request, 'admin_panel/commission_report.html', context)