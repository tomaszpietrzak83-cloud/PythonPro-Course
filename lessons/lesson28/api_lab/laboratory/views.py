import ast
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from .curriculum import EXAMPLES
from .documentation import generated_documentation


def source_code(filename, symbol=None):
    source = (settings.BASE_DIR / filename).read_text(encoding="utf-8")
    if symbol:
        for node in ast.parse(source).body:
            name = getattr(node, "name", None)
            if isinstance(node, ast.Assign):
                name = getattr(node.targets[0], "id", None)
            if name == symbol:
                start = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
                source = "\n".join(source.splitlines()[start - 1:node.end_lineno])
                break
        else:
            raise ValueError(f"Brak symbolu {symbol} w {filename}")
    return {"name": filename, "symbol": symbol or "cały plik", "html": highlight(source, PythonLexer(), HtmlFormatter())}


@ensure_csrf_cookie
def catalog(request):
    return render(request, "laboratory/catalog.html", {"examples": EXAMPLES})


@ensure_csrf_cookie
def lesson(request, number):
    if not 1 <= number <= len(EXAMPLES):
        raise Http404
    item = EXAMPLES[number - 1]
    files = list(dict.fromkeys(path for path, symbol in item["sources"]))
    documentation = generated_documentation()
    for stage in documentation:
        stage["code"] = [source_code("laboratory/comparison_api.py", view.__name__) for view in stage["classes"]]
    return render(request, "laboratory/lesson.html", {
        "item": item, "examples": EXAMPLES,
        "snippets": [source_code(*entry) for entry in item["sources"]],
        "files": [source_code(path) for path in files],
        "next_number": number + 1 if number < len(EXAMPLES) else None,
        "documentation": documentation,
        "serializer_code": source_code("laboratory/serializers.py", "ProductSerializer"),
    })


def health(request):
    return JsonResponse({"app": "lesson28-api-lab", "directory": str(settings.BASE_DIR)})
