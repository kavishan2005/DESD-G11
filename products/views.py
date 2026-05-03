from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    organic = request.GET.get('organic')
    if organic:
        products = products.filter(organic_certified=True)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'organic_filter': organic,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Initialize food_miles
    food_miles = None
    
    # Check if user is authenticated
    if request.user.is_authenticated:
        print(f"User {request.user.username} is authenticated")
        
        # Check if user has profile with postcode
        if hasattr(request.user, 'profile'):
            customer_postcode = request.user.profile.postcode
            print(f"Customer postcode: {customer_postcode}")
            
            # Check if producer has postcode
            if hasattr(product.producer, 'postcode'):
                producer_postcode = product.producer.postcode
                print(f"Producer postcode: {producer_postcode}")
                
                # If both postcodes exist, calculate food miles
                if customer_postcode and producer_postcode:
                    try:
                        # Simple calculation for demo
                        import random
                        random.seed(hash(customer_postcode + producer_postcode) % 100)
                        food_miles = round(random.uniform(2, 25), 1)
                        print(f"Calculated food miles: {food_miles}")
                    except Exception as e:
                        print(f"Error calculating: {e}")
                else:
                    print(f"Missing postcode - customer: {customer_postcode}, producer: {producer_postcode}")
            else:
                print("Producer has no postcode attribute")
        else:
            print("User has no profile")
    else:
        print("User not authenticated")
    
    context = {
        'product': product,
        'food_miles': food_miles,
    }
    return render(request, 'products/product_detail.html', context)

def surplus_deals(request):
    """Display surplus products with discounts"""
    from django.utils import timezone
    
    surplus_products = Product.objects.filter(
        is_surplus=True,
        surplus_expiry__gt=timezone.now(),
        stock_quantity__gt=0
    ).order_by('surplus_expiry')
    
    context = {
        'products': surplus_products,
    }
    return render(request, 'products/surplus_deals.html', context)

def surplus_deals(request):
    """Display surplus products with discounts"""
    from django.utils import timezone
    
    surplus_products = Product.objects.filter(
        is_surplus=True,
        surplus_expiry__gt=timezone.now(),
        stock_quantity__gt=0
    ).order_by('surplus_expiry')
    
    context = {
        'products': surplus_products,
    }
    return render(request, 'products/surplus_deals.html', context)

def surplus_deals(request):
    """Display surplus products with discounts"""
    from django.utils import timezone
    
    surplus_products = Product.objects.filter(
        is_surplus=True,
        surplus_expiry__gt=timezone.now(),
        stock_quantity__gt=0
    ).order_by('surplus_expiry')
    
    context = {
        'products': surplus_products,
    }
    return render(request, 'products/surplus_deals.html', context)
