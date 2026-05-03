from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('surplus/', views.surplus_deals, name='surplus_deals'),  # Must come before slug
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]