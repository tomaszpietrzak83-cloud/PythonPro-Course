from django.urls import path
from learning import views

urlpatterns = [
    path("health/", views.health),
    path("", views.introduction, name="introduction"),
    path("tasks/<int:task_number>/", views.lesson, name="lesson"),
    # TASK 01
    path("tasks/1/run/", views.run_hello, name="run_hello"),
    # TASK 02
    path("tasks/2/run/", views.run_multiply, name="run_multiply"),
    path("tasks/<int:task_number>/run/", views.run_exercise),
    path("tasks/<int:task_number>/data/", views.exercise_data),
    # TASK 11
    path("task-status/<uuid:task_id>/", views.task_status),
    # TASK 14
    path("tasks/status/<uuid:task_id>/", views.task_status, name="task_status"),
]
from django.conf import settings
from django.conf.urls.static import static

# TASK 14
# TASK 16
# TASK 17
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
