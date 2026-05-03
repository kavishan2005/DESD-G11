from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
from products.models import Product, Category, Producer

class ProductModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='producer1',
            password='testpass123',
            email='producer@test.com'
        )
        
        # Create a Producer instance
        self.producer = Producer.objects.create(
            user=self.user,
            farm_name='Test Farm',
            phone='0123456789',
            address='123 Farm Road',
            postcode='BS1 1AA',
            is_active=True
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Vegetables',
            description='Fresh vegetables'
        )
        
        # Create product with slug
        self.product = Product.objects.create(
            name='Organic Carrots',
            slug='organic-carrots',  # Add slug to avoid reverse error
            description='Fresh organic carrots from local farm',
            price=Decimal('2.99'),
            stock_quantity=50,
            availability_status='In Season',
            producer=self.producer,
            category=self.category,
            unit='kg'
        )
    
    def test_product_creation(self):
        """Test product is created correctly"""
        self.assertEqual(self.product.name, 'Organic Carrots')
        self.assertEqual(float(self.product.price), 2.99)
        self.assertEqual(self.product.stock_quantity, 50)
    
    def test_product_str_method(self):
        """Test string representation"""
        self.assertEqual(str(self.product), 'Organic Carrots')
    
    def test_product_list_view(self):
        """Test products page loads"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_view(self):
        """Test product detail page loads using slug"""
        response = self.client.get(f'/products/{self.product.slug}/')
        self.assertEqual(response.status_code, 200)
    
    def test_product_search(self):
        """Test product search works"""
        response = self.client.get('/products/?q=carrots')
        self.assertEqual(response.status_code, 200)
