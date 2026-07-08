from django.urls import path
from . import views

urlpatterns = [
    path("", views.preorder, name="preorder"),
    path("success/", views.preorder_success, name="preorder_success"),
]