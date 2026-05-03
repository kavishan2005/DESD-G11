from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def customer_required(view_func):
    """Decorator to require customer account"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if hasattr(request.user, 'profile') and request.user.profile.user_type != 'customer':
            raise PermissionDenied("This page is for customers only")
        return view_func(request, *args, **kwargs)
    return wrapper

def producer_required(view_func):
    """Decorator to require producer account"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if hasattr(request.user, 'profile') and request.user.profile.user_type != 'producer':
            raise PermissionDenied("This page is for producers only")
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    """Decorator to require admin access"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied("Admin access required")
        return view_func(request, *args, **kwargs)
    return wrapper
