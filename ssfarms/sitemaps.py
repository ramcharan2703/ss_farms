from django.contrib.sitemaps import Sitemap
from django.urls import reverse


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