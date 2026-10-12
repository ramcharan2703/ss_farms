from django.shortcuts import render
from products.models import Category, Product
from gallery.models import Gallery
from testimonials.models import Testimonial


def home(request):
    categories = Category.objects.all()

    # Preload category to avoid N+1 queries when accessing product.category
    products = Product.objects.select_related("category").all()[:6]

    gallery = Gallery.objects.all().order_by("-uploaded_at")

    testimonials = Testimonial.objects.filter(
        is_active=True
    ).order_by("-created_at")

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "gallery": gallery,
        "testimonials": testimonials,
    })