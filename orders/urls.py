from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('producer/orders/', views.producer_orders, name='producer_orders'),
    path('producer/update/<int:suborder_id>/', views.update_order_status, name='update_order_status'),
]
from . import test_view

urlpatterns += [
    path('test/', test_view.test_order_history, name='test_order_history'),
]

urlpatterns += [
    path('history/', views.order_history, name='order_history'),
]

urlpatterns += [
    path('recurring/', views.recurring_orders, name='recurring_orders'),
    path('recurring/create/', views.create_recurring_order, name='create_recurring_order'),
    path('recurring/cancel/<int:recurring_id>/', views.cancel_recurring_order, name='cancel_recurring_order'),
    path('bulk/', views.bulk_order, name='bulk_order'),
]

urlpatterns += [
    path('bulk/', views.bulk_order, name='bulk_order'),
]
