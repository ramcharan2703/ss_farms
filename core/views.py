from django.shortcuts import render
from products.models import Category, Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:6]

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
    })