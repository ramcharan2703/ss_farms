from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product


class ProductCatalogTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fighting Roosters")
        self.product = Product.objects.create(
            category=self.category,
            name="Original Aseel Rooster",
            image="products/test.jpg",
            description="Pure gamecock bloodline description",
            price=12000.00,
            stock=3,
            status="In Stock",
            whatsapp_number="918790733189",
        )

    def test_product_list_loads(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Aseel Rooster")

    def test_product_search(self):
        response = self.client.get(reverse("products") + "?q=Aseel")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Aseel Rooster")

        response = self.client.get(reverse("products") + "?q=NonExistentBreed")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Products Found")

    def test_product_detail_view(self):
        response = self.client.get(reverse("product_detail", kwargs={"id": self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Aseel Rooster")
        self.assertContains(response, "12000")
        # Verify unique SEO title
        self.assertContains(response, "<title>Original Aseel Rooster | SS Farms Wanaparthy</title>")

    def test_product_detail_404_on_invalid_id(self):
        response = self.client.get(reverse("product_detail", kwargs={"id": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_category_protection_on_product_delete(self):
        # Category cannot be deleted if products are associated with it (PROTECT)
        with self.assertRaises(ProtectedError):
            self.category.delete()

    def test_whatsapp_normalization_utility(self):
        from products.validators import normalize_indian_whatsapp_number
        self.assertEqual(normalize_indian_whatsapp_number("8790733189"), "918790733189")
        self.assertEqual(normalize_indian_whatsapp_number("+91 8790733189"), "918790733189")
        self.assertEqual(normalize_indian_whatsapp_number("918790733189"), "918790733189")
        self.assertEqual(normalize_indian_whatsapp_number("08790733189"), "918790733189")
        # Invalid cases
        self.assertIsNone(normalize_indian_whatsapp_number("8"))
        self.assertIsNone(normalize_indian_whatsapp_number("12345"))
        self.assertIsNone(normalize_indian_whatsapp_number(""))
        self.assertIsNone(normalize_indian_whatsapp_number(None))

    def test_product_normalized_whatsapp_fallback(self):
        from django.conf import settings
        business_number = getattr(settings, "WHATSAPP_NUMBER", "918790733189")

        # Valid 10-digit normalizes
        self.product.whatsapp_number = "8790733189"
        self.assertEqual(self.product.normalized_whatsapp_number, "918790733189")

        # Corrupted number "8" falls back safely to business number
        self.product.whatsapp_number = "8"
        self.assertEqual(self.product.normalized_whatsapp_number, business_number)

        # Empty string falls back safely to business number
        self.product.whatsapp_number = ""
        self.assertEqual(self.product.normalized_whatsapp_number, business_number)

        # None falls back safely to business number
        self.product.whatsapp_number = None
        self.assertEqual(self.product.normalized_whatsapp_number, business_number)

        # Test view rendering for product with corrupted "8" number
        Product.objects.filter(id=self.product.id).update(whatsapp_number="8")

        # Product detail view
        detail_res = self.client.get(reverse("product_detail", kwargs={"id": self.product.id}))
        self.assertContains(detail_res, f"https://wa.me/{business_number}?text=")
        self.assertNotContains(detail_res, "https://wa.me/8")

        # Products list view
        list_res = self.client.get(reverse("products"))
        self.assertContains(list_res, f"https://wa.me/{business_number}?text=")
        self.assertNotContains(list_res, "https://wa.me/8")

    def test_product_clean_rejects_corrupted_whatsapp_number(self):
        from django.core.exceptions import ValidationError
        self.product.whatsapp_number = "8"
        with self.assertRaises(ValidationError):
            self.product.clean()

    def test_footer_categories_links_and_filter(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        # Check footer category link points to products with category id
        self.assertContains(response, f'href="/products/?category={self.category.id}"')
        self.assertContains(response, self.category.name)

        # Filter by category
        filter_response = self.client.get(reverse("products") + f"?category={self.category.id}")
        self.assertEqual(filter_response.status_code, 200)
        self.assertContains(filter_response, self.product.name)

    def test_category_cards_render_cleanly_without_description(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        # Verify no empty paragraph for category description
        self.assertNotContains(response, "<p>\n                            \n                        </p>")

