from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product


class CartOperationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Chicks")
        self.product = Product.objects.create(
            category=self.category,
            name="Aseel Day-Old Chick",
            image="products/chick.jpg",
            description="Pure bred fighting chicks",
            price=500.00,
            stock=10,
            status="In Stock",
            whatsapp_number="918790733189",
        )
        self.out_of_stock = Product.objects.create(
            category=self.category,
            name="Rare Champion Chick",
            image="products/rare.jpg",
            description="Sold out",
            price=2000.00,
            stock=0,
            status="Out of Stock",
            whatsapp_number="918790733189",
        )

    def test_state_mutations_require_post(self):
        # GET request to add_to_cart must be rejected (405 Method Not Allowed)
        response = self.client.get(reverse("add_to_cart", kwargs={"product_id": self.product.id}))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse("clear_cart"))
        self.assertEqual(response.status_code, 405)

    def test_add_to_cart_and_total_calculation(self):
        response = self.client.post(reverse("add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 2})
        self.assertEqual(response.status_code, 302)

        # Inspect cart view
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aseel Day-Old Chick")
        self.assertContains(response, "1000.00")  # 500 * 2 = 1000
        self.assertContains(response, "Send Cart on WhatsApp")

    def test_increase_and_decrease_quantity(self):
        # Add 1 item
        self.client.post(reverse("add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 1})

        # Increase
        self.client.post(reverse("increase_quantity", kwargs={"product_id": self.product.id}))
        session = self.client.session
        self.assertEqual(session["cart"][str(self.product.id)], 2)

        # Decrease
        self.client.post(reverse("decrease_quantity", kwargs={"product_id": self.product.id}))
        session = self.client.session
        self.assertEqual(session["cart"][str(self.product.id)], 1)

        # Decrease again (removes item)
        self.client.post(reverse("decrease_quantity", kwargs={"product_id": self.product.id}))
        session = self.client.session
        self.assertNotIn(str(self.product.id), session["cart"])

    def test_out_of_stock_cannot_be_added(self):
        response = self.client.post(reverse("add_to_cart", kwargs={"product_id": self.out_of_stock.id}))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertNotIn(str(self.out_of_stock.id), session.get("cart", {}))

    def test_quantity_boundaries_capped(self):
        # Attempt to add 9999 items
        self.client.post(reverse("add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 9999})
        session = self.client.session
        self.assertEqual(session["cart"][str(self.product.id)], 50)  # Capped at 50

    def test_clear_cart(self):
        self.client.post(reverse("add_to_cart", kwargs={"product_id": self.product.id}))
        self.client.post(reverse("clear_cart"))
        session = self.client.session
        self.assertEqual(session["cart"], {})
