from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Products Listing Page
def product_list(request):

    query = request.GET.get("q")
    category = request.GET.get("category")

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__id=category)

    context = {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": category,
    }

    return render(request, "products.html", context)


# Product Detail Page
def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    return render(request, "product_detail.html", {
        "product": product,
        "related_products": related_products,
    })