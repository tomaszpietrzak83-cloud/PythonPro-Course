answer = """
Standard Django does not provide a universal manage.py command to clear the entire cache.

You can clear it in the Django shell:

from django.core.cache import cache
cache.clear()
"""
