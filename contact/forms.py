import re
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot field for anti-spam bot defense (hidden from human users)
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"style": "display:none;", "autocomplete": "off", "tabindex": "-1"}),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name",
                    "id": "contact_name",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                    "id": "contact_email",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                    "id": "contact_phone",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your message here...",
                    "rows": 5,
                    "id": "contact_message",
                    "required": True,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        # Header injection defense: remove any carriage returns or newlines
        name = re.sub(r"[\r\n]+", " ", name)
        if not name:
            raise forms.ValidationError("Please enter your name.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        # Clean allowed characters: digits, spaces, plus, hyphen
        cleaned_phone = re.sub(r"[^\d+ -]", "", phone)
        digits_only = re.sub(r"\D", "", cleaned_phone)
        if len(digits_only) < 7:
            raise forms.ValidationError("Please enter a valid phone number (at least 7 digits).")
        return cleaned_phone

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("Automated submission detected.")
        return cleaned_data
