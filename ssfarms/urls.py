import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from .views import robots_txt, health_check
from .sitemaps import StaticViewSitemap, ProductSitemap

# Customize Django Admin Portal branding for SS Farms
admin.site.site_header = "SS Farms Wanaparthy Administration"
admin.site.site_title = "SS Farms Admin Portal"
admin.site.index_title = "Farm Management & Operations"

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}

# Allow admin URL path to be customized via environment variable for defense-in-depth
admin_url_path = os.environ.get("ADMIN_URL_PATH", "admin/").strip("/") + "/"

urlpatterns = [
    path("health/", health_check, name="health_check"),

    path(admin_url_path, admin.site.urls),

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
