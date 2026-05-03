from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'amount', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'order__order_number']
