from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from laboratory import api, views
from laboratory.documentation import STAGES, patterns_for

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("examples/<int:number>/", views.lesson, name="lesson"),
    path("health/", views.health),
    path("api/v1/automatic/products/", api.AutomaticProductList.as_view()),
    path("api/v1/docstrings/products/", api.DocstringProductList.as_view()),
    path("api/v1/categories/", api.CategoryList.as_view()),
    path("api/v1/products/", api.ProductListView.as_view()),
    path("api/v1/products/<int:pk>/", api.ProductDetailView.as_view()),
    path("api/v1/sentiment/", api.SentimentView.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

for stage in STAGES:
    key = stage["key"]
    urlpatterns += patterns_for(stage)
    urlpatterns += [
        path(f"documentation/{key}/schema/", SpectacularAPIView.as_view(patterns=patterns_for(stage)), name=f"schema-{key}"),
        path(f"documentation/{key}/swagger/", SpectacularSwaggerView.as_view(url_name=f"schema-{key}"), name=f"swagger-{key}"),
    ]
