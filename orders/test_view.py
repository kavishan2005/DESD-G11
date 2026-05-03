from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def test_order_history(request):
    orders = Order.objects.filter(customer=request.user)
    
    html = f"<h1>Order History Test for {request.user.username}</h1>"
    html += f"<p>Found {orders.count()} orders</p>"
    
    if orders.count() > 0:
        html += "<ul>"
        for order in orders:
            html += f"<li>Order #{order.order_number} - {order.status} - £{order.total}</li>"
        html += "</ul>"
    else:
        html += "<p style='color:red;'>No orders found for this user!</p>"
    
    html += '<p><a href="/orders/history/">Go to regular order history</a></p>'
    
    return HttpResponse(html)
