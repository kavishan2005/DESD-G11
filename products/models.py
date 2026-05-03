from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Producer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producer')
    farm_name = models.CharField(max_length=200)
    farm_description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.farm_name

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_season', 'In Season'),
        ('available', 'Available'),
        ('limited', 'Limited Stock'),
        ('out_of_season', 'Out of Season'),
        ('unavailable', 'Unavailable'),
    ]
    
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit = models.CharField(max_length=50, help_text="e.g., kg, dozen, bunch")
    stock_quantity = models.PositiveIntegerField(default=0)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    
    # Product details
    organic_certified = models.BooleanField(default=False)
    allergen_info = models.TextField(blank=True, help_text="List any allergens")
    
    # Seasonal availability
    season_start_month = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    season_end_month = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    
    # Surplus/Deal fields
    is_surplus = models.BooleanField(default=False)
    surplus_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    surplus_expiry = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def discounted_price(self):
        if self.is_surplus and self.surplus_discount > 0:
            return self.price * (1 - self.surplus_discount / 100)
        return self.price
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= 5
