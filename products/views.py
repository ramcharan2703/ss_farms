from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category and category.isdigit():
        products = products.filter(category__id=int(category))

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "selected_category": category,
    }

    return render(request, "products.html", context)


def product_detail(request, id):
    product = get_object_or_404(Product.objects.select_related("category"), id=id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    ).select_related("category")[:4]

    return render(request, "product_detail.html", {
        "product": product,
        "related_products": related_products,
    })