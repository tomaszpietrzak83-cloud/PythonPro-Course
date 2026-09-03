from datetime import timedelta

from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Article, Category


# --- TASK 03 ---
def category_list_view(request):
    categories = Category.objects.all()
    return render(
        request,
        "myapp/category_list.html",
        {"categories": categories},
    )


# --- TASK 06 07 ---
def category_detail_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles = category.article_set.all().order_by("-pub_date")

    context = {
        "category": category,
        "articles": articles,
    }

    return render(request, "myapp/category_detail.html", context)


# --- TASK 08 10 ---
def article_list_view(request):
    query = request.GET.get("q", "").strip()
    articles = Article.objects.filter(is_published=True)

    if query:
        articles = articles.filter(title__icontains=query)

    articles = articles.order_by("-pub_date")
    recent_threshold = timezone.now() - timedelta(days=3)

    context = {
        "articles": articles,
        "query": query,
        "recent_threshold": recent_threshold,
    }

    return render(request, "myapp/article_list.html", context)
