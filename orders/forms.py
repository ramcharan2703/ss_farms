import re
from django import forms
from django.utils import timezone
from .models import PreOrder


class PreOrderForm(forms.ModelForm):
    class Meta:
        model = PreOrder
        fields = [
            "customer_name",
            "phone_number",
            "product",
            "quantity",
            "preferred_date",
            "address",
            "notes",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "id": "preorder_name",
                "required": True,
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter 10-digit WhatsApp phone number",
                "id": "preorder_phone",
                "required": True,
            }),
            "product": forms.Select(attrs={
                "class": "form-select",
                "id": "preorder_product",
                "required": True,
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 500,
                "value": 1,
                "id": "preorder_quantity",
                "required": True,
            }),
            "preferred_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
                "id": "preorder_date",
                "required": True,
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter delivery village / town / district and state",
                "id": "preorder_address",
                "required": True,
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Specific bloodline or age preference (optional)",
                "id": "preorder_notes",
            }),
        }

    def clean_customer_name(self):
        name = self.cleaned_data.get("customer_name", "").strip()
        name = re.sub(r"[\r\n]+", " ", name)
        if not name:
            raise forms.ValidationError("Please provide your name.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number", "").strip()
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 7:
            raise forms.ValidationError("Please enter a valid phone number with at least 7 digits.")
        return phone

    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity")
        if not qty or qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        if qty > 500:
            raise forms.ValidationError("For bulk orders over 500 units, please contact us directly on WhatsApp.")
        return qty

    def clean_preferred_date(self):
        date = self.cleaned_data.get("preferred_date")
        if date and date < timezone.now().date():
            raise forms.ValidationError("Preferred delivery date cannot be in the past.")
        return date