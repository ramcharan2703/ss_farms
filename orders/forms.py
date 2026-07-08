from django import forms
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
                "placeholder": "Enter your name"
            }),

            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number"
            }),

            "product": forms.Select(attrs={
                "class": "form-select"
            }),

            "quantity": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "preferred_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter your address"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Additional notes (optional)"
            }),
        }