from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, SubOrder

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user', 'is_active', 'item_count', 'created_at']
    list_filter = ['is_active']
    search_fields = ['user__username']
    
    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return "Anonymous"
    get_user.short_description = 'User'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
    list_filter = ['cart__is_active']
    search_fields = ['product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'delivery_date', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer__username']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'status', 'delivery_date')
        }),
        ('Delivery Details', {
            'fields': ('delivery_address', 'delivery_instructions')
        }),
        ('Financial', {
            'fields': ('subtotal', 'commission', 'total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'unit_price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'product__name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product', 'producer')

@admin.register(SubOrder)
class SubOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'producer', 'status', 'subtotal', 'delivery_date']
    list_filter = ['status', 'delivery_date']
    search_fields = ['order__order_number', 'producer__farm_name']
