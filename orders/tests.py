from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Category, Producer
from orders.models import Order, OrderItem
from decimal import Decimal
from datetime import datetime, timedelta

class OrderModelTest(TestCase):
    def setUp(self):
        # Create customer
        self.customer = User.objects.create_user(
            username='customer1',
            password='testpass123',
            email='customer@test.com'
        )
        
        # Create producer user
        producer_user = User.objects.create_user(
            username='producer1',
            password='testpass123',
            email='producer@test.com'
        )
        
        # Create Producer instance
        self.producer = Producer.objects.create(
            user=producer_user,
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
        
        # Create product
        self.product = Product.objects.create(
            name='Tomatoes',
            description='Fresh tomatoes',
            price=Decimal('3.50'),
            stock_quantity=100,
            availability_status='In Season',
            producer=self.producer,
            category=self.category,
            unit='kg'
        )
        
        # Create order
        self.order = Order.objects.create(
            order_number='ORD-001',
            customer=self.customer,
            delivery_address='45 Park Street, Bristol, BS1 5JG',
            delivery_date=datetime.now().date() + timedelta(days=3),
            status='pending',
            subtotal=Decimal('3.50'),
            commission=Decimal('0.18'),
            total=Decimal('3.68')
        )
        
        # Create order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=Decimal('3.50')
        )
    
    def test_order_creation(self):
        """Test order is created correctly"""
        self.assertEqual(self.order.order_number, 'ORD-001')
        self.assertEqual(self.order.customer.username, 'customer1')
        self.assertEqual(float(self.order.subtotal), 3.50)
        self.assertEqual(self.order.status, 'pending')
        self.assertIsNotNone(self.order.delivery_date)
    
    def test_order_item_creation(self):
        """Test order item is created"""
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(float(self.order_item.unit_price), 3.50)
        self.assertEqual(self.order_item.product.name, 'Tomatoes')
    
    def test_order_total_calculation(self):
        """Test order total includes subtotal + commission"""
        expected_total = self.order.subtotal + self.order.commission
        self.assertEqual(float(self.order.total), float(expected_total))
    
    def test_cart_page_exists(self):
        """Test cart page exists at /orders/cart/"""
        self.client.login(username='customer1', password='testpass123')
        response = self.client.get('/orders/cart/')  # Fixed: Added orders/ prefix
        self.assertEqual(response.status_code, 200)  # Should be 200, not just not 404
