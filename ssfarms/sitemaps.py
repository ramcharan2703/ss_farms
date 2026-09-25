from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from products.models import Product


class StaticViewSitemap(Sitemap):

    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "products",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse(
            "product_detail",
            kwargs={"id": obj.id}
        )