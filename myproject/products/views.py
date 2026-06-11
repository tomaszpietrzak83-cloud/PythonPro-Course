from django.http import HttpResponse
from django.shortcuts import redirect, render

from products.models import Category, Product

from .forms import ProductForm


# --- TASK 01 ---
def info(request):
    return HttpResponse("Informacje o stronie")


# --- TASK 01 ---
def rules(request):
    return HttpResponse("Regulamin")


# --- TASK 02 ---
def user_greeting(request, username):
    return HttpResponse(f"Witaj, {username}!")


# --- TASK 04 ---
def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


# --- TASK 07 ---
def product_creation(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products:product_list")
    else:
        form = ProductForm()

    return render(request, "create_product.html", {"form": form})


# --- TASK 09 ---
def category_view(request, category_id):
    products = Product.objects.filter(category_id=category_id).all()
    return render(request, "sort_by_category.html", {"products": products})
