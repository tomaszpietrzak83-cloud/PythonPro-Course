from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date

from .models import Author, Category, Post, Tag


# TASK 03 06
def post_views(request):
    query = request.GET.get("q", "").strip()
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-publication_date")
    else:
        posts = Post.objects.order_by("-publication_date")[:5]

    return render(request, "post_views.html", {"posts": posts, "query": query})


# TASK 02
def category(request, category_id):
    posts = Post.objects.filter(category_id=category_id)
    return render(request, "sort_by_category.html", {"posts": posts})


def _clean_values(query_dict, name):
    """Return unique, non-empty repeated query-string values."""
    return list(
        dict.fromkeys(
            value.strip() for value in query_dict.getlist(name) if value.strip()
        )
    )


def _author_query(author_terms):
    query = Q()
    for term in author_terms:
        words = term.split()
        term_query = Q(author__first_name__icontains=term) | Q(
            author__last_name__icontains=term
        )
        if len(words) > 1:
            term_query |= Q(author__first_name__icontains=words[0]) & Q(
                author__last_name__icontains=" ".join(words[1:])
            )
        # ***
        query |= term_query
    return query


def _matching_score(post, keywords, tag_terms):
    """Return (matched criteria, all criteria) for one post."""
    searchable_text = f"{post.title} {post.content}".casefold()
    post_tags = [tag.name.casefold() for tag in post.tags.all()]
    matched_keywords = sum(
        term.casefold() in searchable_text for term in keywords
    )
    matched_tags = sum(
        any(term.casefold() in tag_name for tag_name in post_tags)
        for term in tag_terms
    )
    return matched_keywords + matched_tags, len(keywords) + len(tag_terms)


def _query_without_page(request):
    # request.GET is an immutable QueryDict, so make an editable copy first.
    query = request.GET.copy()
    # Remove the current page number but keep every active search filter.
    # The default None prevents an error when the URL has no "page" parameter.
    query.pop("page", None)
    # Convert the remaining parameters back to URL form. QueryDict.urlencode()
    # also preserves repeated values such as author=Tom&author=Jane.
    return query.urlencode()


# SEARCH-SITE: One GET endpoint owns the form, filters, scoring and pagination.
def article_search(request):
    author_terms = _clean_values(request.GET, "author")
    tag_terms = _clean_values(request.GET, "tag")
    keywords = _clean_values(request.GET, "keyword")
    category_ids = _clean_values(request.GET, "category")
    date_from = request.GET.get("from", "").strip()
    date_to = request.GET.get("to", "").strip()
    submitted = bool(request.GET)
    errors = []

    posts = Post.objects.select_related("author", "category").prefetch_related(
        "tags"
    )

    parsed_from = parse_date(date_from) if date_from else None
    parsed_to = parse_date(date_to) if date_to else None
    if date_from and parsed_from is None:
        errors.append("The start date is invalid.")
    if date_to and parsed_to is None:
        errors.append("The end date is invalid.")
    if parsed_from and parsed_to and parsed_from > parsed_to:
        errors.append("The start date cannot be later than the end date.")

    if parsed_from:
        posts = posts.filter(publication_date__date__gte=parsed_from)
    if parsed_to:
        posts = posts.filter(publication_date__date__lte=parsed_to)
    if category_ids:
        posts = posts.filter(category_id__in=category_ids)
    if author_terms:
        posts = posts.filter(_author_query(author_terms))

    results = []
    if submitted and not errors:
        for post in posts.distinct().order_by("-publication_date"):
            matched, total = _matching_score(post, keywords, tag_terms)
            if total and matched == 0:
                continue
            post.match_count = matched
            post.criteria_count = total
            post.match_percent = round(matched / total * 100) if total else None
            results.append(post)

        if keywords or tag_terms:
            results.sort(
                key=lambda post: (post.match_percent, post.publication_date),
                reverse=True,
            )

    page_obj = Paginator(results, 5).get_page(request.GET.get("page"))
    context = {
        "categories": Category.objects.order_by("name"),
        "selected_categories": category_ids,
        "author_terms": author_terms,
        "tag_terms": tag_terms,
        "keywords": keywords,
        "date_from": date_from,
        "date_to": date_to,
        "submitted": submitted,
        "errors": errors,
        "page_obj": page_obj,
        "result_count": len(results),
        "pagination_query": _query_without_page(request),
        "current_query": request.GET.urlencode(),
        "highlight_data": {
            "keywords": keywords,
            "authors": author_terms,
            "tags": tag_terms,
        },
    }
    return render(request, "article_search.html", context)


# SEARCH-SITE: Small JSON endpoints feed Tom Select after three characters.
def author_suggestions(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 1:
        return JsonResponse([], safe=False)
    authors = Author.objects.filter(is_placeholder=False).filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )[:10]
    return JsonResponse(
        [
            {"value": author.full_name, "text": author.full_name}
            for author in authors
        ],
        safe=False,  # list not dict, so safe=False
    )


def tag_suggestions(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 1:
        return JsonResponse([], safe=False)
    tags = Tag.objects.filter(name__icontains=query).order_by("name")[:10]
    return JsonResponse(
        [{"value": tag.name, "text": tag.name} for tag in tags], safe=False
    )


def article_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author", "category").prefetch_related(
            "tags"
        ),
        pk=post_id,
    )
    highlight_data = {
        "keywords": _clean_values(request.GET, "keyword"),
        "authors": _clean_values(request.GET, "author"),
        "tags": _clean_values(request.GET, "tag"),
    }
    return render(
        request,
        "article_detail.html",
        {
            "post": post,
            "highlight_data": highlight_data,
            "back_query": request.GET.urlencode(),
        },
    )


def search_help(request):
    return render(request, "search_help.html")
