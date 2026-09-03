from django.urls import path

from . import views

app_name = "myapp2"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
]
