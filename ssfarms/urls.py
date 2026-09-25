from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from .views import robots_txt
from .sitemaps import StaticViewSitemap, ProductSitemap
sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    path("products/", include("products.urls")),

    path("preorders/", include("orders.urls")),

    path("contact/", include("contact.urls")),

    path("inquiry/", include("inquiry.urls")),

    path("robots.txt", robots_txt),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )