from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),      # ONCE only
    path('admin-panel/', include('admin_panel.urls')),  # ONCE only
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')),
]