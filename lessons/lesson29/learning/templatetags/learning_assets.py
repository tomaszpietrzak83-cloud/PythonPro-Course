from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def versioned_static(filename):
    """A changed local asset gets a fresh URL, even with browser caching."""
    path = settings.BASE_DIR / "learning/static" / filename
    return f"{static(filename)}?v={path.stat().st_mtime_ns}"
