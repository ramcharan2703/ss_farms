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
