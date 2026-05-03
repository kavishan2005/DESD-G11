from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-intent/<int:order_id>/', views.create_payment_intent, name='create_payment_intent'),
    path('page/<int:order_id>/', views.payment_page, name='payment_page'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),
]
