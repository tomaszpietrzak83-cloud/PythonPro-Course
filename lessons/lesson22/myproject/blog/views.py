from django.db.models import Q
from django.shortcuts import render

from .models import Post


# TASK 03 06
def post_views(request):
    # TASK 06
    query = request.GET.get("q", "").strip()
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-publication_date")

    else:
        # TASK 03
        posts = Post.objects.order_by("-publication_date")[:5]

    return render(request, "post_views.html", {"posts": posts, "query": query})


# TASK 02
def category(request, category_id):
    posts = Post.objects.filter(category_id=category_id)
    return render(request, "sort_by_category.html", {"posts": posts})
