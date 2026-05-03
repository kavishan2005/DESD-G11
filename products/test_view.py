from django.http import HttpResponse
from .models import Product

def test_products(request):
    products = Product.objects.all()
    output = "<h1>Products in Database</h1>"
    output += f"<p>Total products: {products.count()}</p>"
    output += "<ul>"
    for product in products:
        output += f"<li>{product.name} - £{product.price} - {product.category.name if product.category else 'No category'}</li>"
    output += "</ul>"
    output += '<p><a href="/admin/">Go to Admin</a></p>'
    return HttpResponse(output)
