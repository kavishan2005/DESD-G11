# 🍅 Bristol Food Network Marketplace

![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing-brightgreen)

## 📖 About The Project

The **Bristol Food Network Marketplace** is an e-commerce platform connecting local food producers with customers in the Bristol area. Built with Django, this platform enables producers to list their products and customers to browse, purchase, and track locally sourced food.

### 🎯 Problem Statement
Small-scale local producers struggle to reach customers beyond farmers' markets. Third-party marketplaces charge high commissions and provide limited visibility. This platform eliminates the intermediary, allowing producers to retain more revenue and customers to access fresh local produce with clear provenance.

### ✨ Key Features

#### 👥 Customer Features
- User registration and authentication
- Browse products by category
- Search products by name or description
- Shopping cart with session persistence
- Secure checkout with delivery information
- Order confirmation and history tracking

#### 👨‍🌾 Producer Features
- Dedicated producer dashboard
- Product listing management
- View incoming orders
- Commission calculation (5% network fee)

#### 🔒 Security Features
- Password hashing (PBKDF2)
- Role-based access control (Customer/Producer/Admin)
- CSRF protection on all forms
- SQL injection prevention via Django ORM
- Session management

---

## 🏗️ System Architecture
┌─────────────────────────────────────────────────────────────────┐
│ DJANGO MVT ARCHITECTURE │
├─────────────────────────────────────────────────────────────────┤
│ │
│ Browser → URL Dispatcher → View → Model → Database │
│ │
│ Browser ← Template ← View ← Model ← Database │
│ │
├─────────────────────────────────────────────────────────────────┤
│ 📁 accounts/ - User registration, login, roles │
│ 📁 products/ - Product catalogue, search, categories │
│ 📁 orders/ - Shopping cart, checkout, order history │
│ 📁 payments/ - Payment calculations, commission reports │
│ 📁 dashboard/ - Producer management interface │
└─────────────────────────────────────────────────────────────────┘

text

### Database Schema
User ──── Producer ──── Product ──── OrderItem ──── Order
│ │ │ │ │
│ │ │ │ │
└──────────┴────────────┴──────────────┴────────────┘
Foreign Key Relationships

text

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.12+ |
| Docker | 20.10+ (optional) |
| pip | Latest |
| Git | Latest |

### 📦 Installation

#### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/kavishan2005/DESD-G11.git
   cd DESD-G11
Create and activate virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Run migrations

bash
python manage.py migrate
Create superuser (admin)

bash
python manage.py createsuperuser
Run development server

bash
python manage.py runserver
Access the application

Website: http://127.0.0.1:8000/
Admin panel: http://127.0.0.1:8000/admin/
Option 2: Docker Deployment (Recommended)

bash
# Build and run containers
docker-compose up --build

# Access at: http://localhost:8000
🧪 Running Tests

bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test accounts
python manage.py test products
python manage.py test orders
Test Results

text
✅ 12/12 tests passing
- accounts: 3 tests
- products: 5 tests  
- orders: 4 tests
👥 User Roles

Role	Access	Permissions
Customer	/products/, /orders/cart/, /orders/checkout/	Browse, cart, checkout, order history
Producer	/dashboard/, /admin/ (limited)	Add/edit products, view orders, commission reports
Admin	/admin/	Full system control, user management
Demo Accounts

Role	Username	Password	Access
Admin	admin	(created during setup)	Full admin panel
Producer	producer	producer123	Dashboard + limited admin
Customer	(register new)	(user defined)	Customer features only
🔐 Security Implementation

Security Feature	Implementation
Password Storage	PBKDF2 hashing (Django default)
Role-Based Access	@login_required decorator + role checks
CSRF Protection	{% csrf_token %} on all forms
SQL Injection	Django ORM parameterised queries
Session Security	Secure session cookie handling
Role-Based Access Example

python
@login_required
def add_product(request):
    if request.user.role != 'producer':
        raise PermissionDenied()
    # Producer-only code here
📂 Project Structure

text
DESD-G11/
├── accounts/              # User authentication & role management
│   ├── models.py          # Custom User model
│   ├── views.py           # Registration, login, profile
│   └── urls.py            # Auth routes
├── products/              # Product catalogue
│   ├── models.py          # Product, Category, Producer
│   ├── views.py           # Product list, detail, search
│   └── urls.py            # Product routes
├── orders/                # Cart & checkout
│   ├── models.py          # Order, OrderItem
│   ├── views.py           # Cart, checkout, history
│   └── urls.py            # Order routes
├── payments/              # Payment calculations
│   ├── models.py          # Payment model
│   └── views.py           # Commission reports
├── dashboard/             # Producer dashboard
│   └── views.py           # Producer management
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── */                 # App-specific templates
├── static/                # CSS, JS, images
├── config/                # Django settings
│   ├── settings.py        # Project configuration
│   └── urls.py            # Main URL configuration
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Multi-container orchestration
├── requirements.txt       # Python dependencies
├── manage.py              # Django CLI
└── README.md              # This file
🐳 Docker Containerisation

Dockerfile

dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
docker-compose.yml

yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=0
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
🧪 Test Cases Covered

TC#	Feature	Status
TC-001	Customer Registration	✅
TC-002	Customer Login	✅
TC-003	Producer Add Product	✅
TC-004	Browse Categories	✅
TC-005	Search Products	✅
TC-006	Shopping Cart	✅
TC-007	Single Vendor Order	✅
TC-021	Order History	✅
TC-022	Security (Role-Based Access)	✅
🔧 Troubleshooting

Common Issues & Solutions

Issue	Solution
Port 8000 already in use	lsof -i :8000 then kill -9 [PID]
Migrations not applying	python manage.py migrate --run-syncdb
Docker permission denied	Start Docker Desktop or run colima start
Test database error	python manage.py test --keepdb
📈 Future Improvements

Priority	Feature	Description
High	Stripe Integration	Real payment processing
High	Automated Tests	Comprehensive test suite
Medium	Responsive Design	Mobile-friendly UI
Medium	PostgreSQL	Production database
Low	Email Notifications	Order confirmations
Low	Food Miles	Sustainability tracking
👥 Contributors

Name	Student ID	Role	Contribution
Kavishan Wasantha Kumar	23010875	Lead Developer	55%
Youssef Ahmed Aboubakr	23056152	Frontend Developer	25%
Sandaru Induwara Hewa Madihage	22060272	Documentation	20%
