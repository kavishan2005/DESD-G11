from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class DashboardStats(models.Model):
    """Dashboard statistics cache"""
    date = models.DateField(auto_now_add=True)
    total_users = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = "Dashboard Stats"
