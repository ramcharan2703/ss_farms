from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        send_mail(
            subject=f"📩 New Contact Message from {name}",
            message=f"""
New Inquiry Received

Date: {timezone.now().strftime('%d-%m-%Y %I:%M %p')}

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
""",
            from_email=None,
            recipient_list=["ssfarmswanaparthy@gmail.com"],
            fail_silently=False,
        )

        messages.success(
            request,
            "Your message has been sent successfully!"
        )

        return redirect("contact")

    return render(request, "contact.html")