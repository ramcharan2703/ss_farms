from django.shortcuts import render
from gallery.models import Gallery

def home(request):
    gallery = Gallery.objects.all().order_by("-uploaded_at")

    return render(request, "home.html", {
        "gallery": gallery,
    })
# Create your views here.
