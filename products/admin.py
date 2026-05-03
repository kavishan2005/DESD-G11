from django.contrib import admin
from .models import Category, Product, Producer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ['farm_name', 'user', 'is_active']
    list_filter = ['is_active']
    search_fields = ['farm_name', 'user__username']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'producer', 'category', 'price', 'stock_quantity', 'availability_status']
    list_filter = ['availability_status', 'organic_certified', 'category']
    search_fields = ['name', 'producer__farm_name']
    prepopulated_fields = {'slug': ('name',)}
