from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.all()

    context = {
        "products": products
    }

    return render(request, "home.html", context)