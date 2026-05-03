from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

class Notification(TimeStampedModel):
    NOTIFICATION_TYPES = (
        ('order_confirmed', 'Order Confirmed'),
        ('order_status', 'Order Status Update'),
        ('low_stock', 'Low Stock Alert'),
        ('payment_received', 'Payment Received'),
        ('new_review', 'New Review'),
        ('surplus_expiring', 'Surplus Deal Expiring'),
        ('recurring_order', 'Recurring Order'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"