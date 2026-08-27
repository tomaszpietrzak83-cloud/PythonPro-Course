from django.contrib import admin
from django.urls import include, path
from new_app import views
from rest_framework import routers

router = routers.DefaultRouter()
# TASK 03 08
router.register(r"products", views.ProductViewSet)

# TASK 06
router.register(r"notes", views.NoteViewSet)

# TASK 09
router.register(r"authors", views.AuthorViewSet)

# TASK 09
router.register(r"books", views.BookViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # TASK 05
    path("api/set-name/", views.set_name),
    # TASK 05
    path("api/hello/", views.hello),
    # TASK 07
    path("api/calculate/", views.calculate),
    # TASK 08
    path("api/filter-products/", views.filter_by_price),
]
