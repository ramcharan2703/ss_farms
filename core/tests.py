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

    def test_clickable_contact_and_social_links(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="tel:+918790733189"')
        self.assertContains(response, 'href="mailto:ssfarmswanaparthy@gmail.com"')
        self.assertContains(response, 'href="https://wa.me/918790733189"')
        self.assertContains(response, 'href="https://www.facebook.com/profile.php?id=61586339823753"')
        # Ensure neither Facebook nor WhatsApp are dead links
        self.assertNotContains(response, 'href="#"')



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

    def test_message_tag_rendering(self):
        from django.test import RequestFactory
        from django.template import Context, Template
        from django.contrib.messages.storage.base import Message
        from django.contrib.messages import constants as msg_constants

        rf = RequestFactory()
        request = rf.get("/", HTTP_HOST="127.0.0.1")
        t = Template('{% extends "base.html" %}')

        test_cases = [
            (msg_constants.ERROR, "", "alert-danger"),
            (msg_constants.WARNING, "", "alert-warning"),
            (msg_constants.SUCCESS, "", "alert-success"),
            (msg_constants.INFO, "", "alert-info"),
            (msg_constants.DEBUG, "", "alert-secondary"),
            (msg_constants.INFO, "danger", "alert-danger"),
            (999, "unknown_custom_tag", "alert-info"),
            (999, "", "alert-info"),
        ]

        for level, extra_tags, expected_cls in test_cases:
            msg = Message(level=level, message=f"Test message for level {level}", extra_tags=extra_tags)
            rendered = t.render(Context({"messages": [msg], "request": request}))
            self.assertIn(expected_cls, rendered, f"Level {level} with tag '{extra_tags}' did not produce '{expected_cls}'")
            if level == msg_constants.ERROR or "danger" in extra_tags:
                self.assertNotIn("alert-success", rendered, f"Error message should not produce 'alert-success'")

    def test_navbar_active_states_across_routes(self):
        # 1. Home
        res = self.client.get(reverse("home"))
        self.assertContains(res, 'class="nav-link active"\n                           href="/"\n                           aria-current="page"')

        # 2. Products List
        res = self.client.get(reverse("products"))
        self.assertContains(res, 'class="nav-link active"\n                           href="/products/"\n                           aria-current="page"')
        # Ensure Home is NOT active on products page
        self.assertNotContains(res, 'class="nav-link active"\n                           href="/"')

        # 3. Product Detail
        res = self.client.get(reverse("product_detail", kwargs={"id": self.product.id}))
        self.assertContains(res, 'class="nav-link active"\n                           href="/products/"\n                           aria-current="page"')
        self.assertNotContains(res, 'class="nav-link active"\n                           href="/"')

        # 4. Contact
        res = self.client.get(reverse("contact"))
        self.assertContains(res, 'class="nav-link active"\n                           href="/contact/"\n                           aria-current="page"')
        self.assertNotContains(res, 'class="nav-link active"\n                           href="/"')

        # 5. Cart
        res = self.client.get(reverse("cart"))
        self.assertContains(res, 'class="nav-link position-relative active"\n                           href="/inquiry/"\n                           aria-current="page"')
        self.assertNotContains(res, 'class="nav-link active"\n                           href="/"')

        # 6. Preorder
        res = self.client.get(reverse("preorder"))
        self.assertContains(res, 'href="/preorders/"\n                           class="btn btn-success rounded-pill px-4 active shadow"\n                           aria-current="page"')
        self.assertNotContains(res, 'class="nav-link active"\n                           href="/"')



