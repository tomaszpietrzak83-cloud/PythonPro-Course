from django.urls import path

from . import views

app_name = "myapp3"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
]
