from datetime import date, timedelta
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from orders.models import PreOrder
from products.models import Category, Product


class PreOrderTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Hatching Eggs")
        self.product = Product.objects.create(
            category=self.category,
            name="Fertile Bheemavaram Eggs",
            image="products/egg.jpg",
            description="Pure bloodline fertile eggs",
            price=250.00,
            stock=50,
            status="In Stock",
            whatsapp_number="918790733189",
        )

    def test_preorder_form_loads(self):
        response = self.client.get(reverse("preorder"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pre-Order Form")

    def test_valid_preorder_submission(self):
        future_date = date.today() + timedelta(days=14)
        data = {
            "customer_name": "Suresh Reddy",
            "phone_number": "918790733189",
            "product": self.product.id,
            "quantity": 10,
            "preferred_date": future_date.strftime("%Y-%m-%d"),
            "address": "Wanaparthy Town, Telangana",
            "notes": "Please pack with extra cushioning",
        }
        response = self.client.post(reverse("preorder"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("preorder_success"))

        order = PreOrder.objects.filter(customer_name="Suresh Reddy").first()
        self.assertIsNotNone(order)
        self.assertEqual(order.quantity, 10)

    def test_past_date_rejected(self):
        past_date = date.today() - timedelta(days=2)
        data = {
            "customer_name": "Suresh Reddy",
            "phone_number": "918790733189",
            "product": self.product.id,
            "quantity": 5,
            "preferred_date": past_date.strftime("%Y-%m-%d"),
            "address": "Hyderabad",
            "notes": "",
        }
        response = self.client.post(reverse("preorder"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PreOrder.objects.count(), 0)
        self.assertContains(response, "alert-danger")
        self.assertNotContains(response, "alert-success")


    def test_preorder_success_contains_correct_whatsapp_number(self):
        response = self.client.get(reverse("preorder_success"))
        self.assertEqual(response.status_code, 200)
        # Verify correct number 918790733189 and absence of typo 918790733178
        self.assertContains(response, "918790733189")
        self.assertNotContains(response, "918790733178")

    def test_product_protected_against_accidental_cascade_delete(self):
        future_date = date.today() + timedelta(days=7)
        PreOrder.objects.create(
            customer_name="Customer",
            phone_number="9876543210",
            product=self.product,
            quantity=2,
            preferred_date=future_date,
            address="Wanaparthy",
        )
        # Attempting to delete the product must be blocked by PROTECT
        with self.assertRaises(ProtectedError):
            self.product.delete()
