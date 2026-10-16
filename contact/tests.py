from django.test import TestCase
from django.urls import reverse
from contact.models import ContactMessage


class ContactFormTests(TestCase):
    def test_contact_page_loads(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send Us a Message")
        self.assertContains(response, 'href="tel:+918790733189"')
        self.assertContains(response, 'href="mailto:ssfarmswanaparthy@gmail.com"')
        self.assertContains(response, 'href="https://wa.me/918790733189"')


    def test_valid_contact_submission_persisted_in_db(self):
        data = {
            "name": "Ramesh Kumar",
            "email": "ramesh@example.com",
            "phone": "9876543210",
            "message": "I am interested in buying 5 hatching eggs.",
            "website": "",  # Honeypot empty
        }
        response = self.client.post(reverse("contact"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your inquiry has been received successfully")

        # Verify record exists in database
        inquiry = ContactMessage.objects.filter(email="ramesh@example.com").first()
        self.assertIsNotNone(inquiry)
        self.assertEqual(inquiry.name, "Ramesh Kumar")
        self.assertEqual(inquiry.phone, "9876543210")

    def test_invalid_email_rejected(self):
        data = {
            "name": "Ramesh",
            "email": "not-a-valid-email",
            "phone": "9876543210",
            "message": "Hello",
            "website": "",
        }
        response = self.client.post(reverse("contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_honeypot_rejects_bots(self):
        data = {
            "name": "Spam Bot",
            "email": "bot@spam.com",
            "phone": "9876543210",
            "message": "Spam content",
            "website": "http://spamsite.com",  # Honeypot filled by bot
        }
        response = self.client.post(reverse("contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
