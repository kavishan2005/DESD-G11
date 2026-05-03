from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from products.models import Product, Producer
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart {self.id} - {self.user.username}"
        return f"Cart {self.id} - Session {self.session_id}"
    
    @property
    def total(self):
        items = self.items.all()
        if items:
            return sum(item.subtotal for item in items)
        return 0
    
    @property
    def item_count(self):
        return self.items.count()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        if self.product and self.product.price and self.quantity:
            return self.product.price * self.quantity
        return 0

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_address = models.TextField()
    delivery_date = models.DateField()
    delivery_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Financial
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Unknown'}"
    
    @property
    def subtotal(self):
        if self.unit_price and self.quantity:
            return self.unit_price * self.quantity
        return 0

class SubOrder(models.Model):
    """Separate orders for each producer in multi-vendor orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='suborders')
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    producer_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"SubOrder for {self.producer} - Order {self.order.order_number}"

class RecurringOrder(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_orders')
    name = models.CharField(max_length=100, default="My Weekly Order")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    next_delivery_date = models.DateField()
    delivery_instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.customer.username} ({self.frequency})"
    
    def generate_next_order(self):
        """Generate the next order based on frequency"""
        from datetime import timedelta
        if self.frequency == 'weekly':
            return self.next_delivery_date + timedelta(days=7)
        elif self.frequency == 'biweekly':
            return self.next_delivery_date + timedelta(days=14)
        else:  # monthly
            # Simple monthly calculation
            if self.next_delivery_date.month == 12:
                return self.next_delivery_date.replace(year=self.next_delivery_date.year + 1, month=1)
            else:
                return self.next_delivery_date.replace(month=self.next_delivery_date.month + 1)

class RecurringOrderItem(models.Model):
    recurring_order = models.ForeignKey(RecurringOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity

class RecurringOrder(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_orders')
    name = models.CharField(max_length=100, default="My Weekly Order")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    next_delivery_date = models.DateField()
    delivery_instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.customer.username} ({self.frequency})"

class RecurringOrderItem(models.Model):
    recurring_order = models.ForeignKey(RecurringOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity


class RecurringOrder(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_orders')
    name = models.CharField(max_length=100, default="My Weekly Order")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    next_delivery_date = models.DateField()
    delivery_instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.customer.username} ({self.frequency})"

class RecurringOrderItem(models.Model):
    recurring_order = models.ForeignKey(RecurringOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity