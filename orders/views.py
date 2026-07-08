from django.shortcuts import render, redirect
from .forms import PreOrderForm


def preorder(request):

    if request.method == "POST":

        form = PreOrderForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("preorder_success")

    else:

        form = PreOrderForm()

    return render(request, "preorder.html", {
        "form": form
    })
def preorder_success(request):
    return render(request, "preorder_success.html")