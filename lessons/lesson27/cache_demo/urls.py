"""Use identical URLs on each port; task pages execute in their own process."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="demo_home"),
    path("task/<int:number>/", views.task, name="demo_task"),
    path("demo/health/", views.health, name="demo_health"),
    path("demo/api/<int:number>/", views.action, name="demo_action"),
]
