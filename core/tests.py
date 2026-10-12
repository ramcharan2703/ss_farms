import os
from django.test import TestCase, override_settings
from django.urls import reverse
from products.models import Category, Product


class CoreAndSeoTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Aseel Roosters")
        self.product = Product.objects.create(
            category=self.category,
            name="Bhimavaram Pure Rooster",
            image="products/test.jpg",
            description="Pure breed rooster description",
            price=15000.00,
            stock=2,
            status="In Stock",
            whatsapp_number="918790733189",
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SS Farms")
        self.assertContains(response, "Bhimavaram Pure Rooster")

    def test_health_check_endpoint(self):
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["app"], "ssfarms")
        self.assertEqual(data["database"], "connected")

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Disallow: /inquiry/")
        self.assertContains(response, "Sitemap:")

    def test_sitemap_xml(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/products/")
        self.assertContains(response, f"/products/{self.product.id}/")

    def test_custom_404_page(self):
        response = self.client.get("/non-existent-random-url-path-999/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Page Not Found", status_code=404)
        self.assertContains(response, "404", status_code=404)
