outcome = """
python manage.py shell
13 objects imported automatically (use -v 2 for details).

Ctrl click to launch VS Code Native REPL
Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.core.cache import cache
>>> cache.set("my_key", "hello world", 30)
>>> cache.get("my_key")
'hello world'
>>> cache.set("my_key", "hello world", 3) 
>>> cache.get("my_key")
>>> cache.get("my_key")
>>> cache.set("my_key", "hello world", 3)
>>> cache.get("my_key")
'hello world'
>>> cache.get("my_key")
"""
