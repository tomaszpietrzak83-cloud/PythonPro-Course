from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^zadania/(?P<task_number>0[1-9]|10)/$", views.task_detail, name="task_detail"),
    path("admin/", admin.site.urls),
]
