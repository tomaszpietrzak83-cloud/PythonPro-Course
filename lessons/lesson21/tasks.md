# Lesson21 Tasks

This file is a compact task list for the implemented Django project.

1. Create the `Category` model with a `name` field.
2. Create three category objects: `Sport`, `Technology`, `Culture`.
3. Display all categories at `/categories/`.
4. Add and load a CSS file for the category list.
5. Query the `Sport` category with `Category.objects.get(name="Sport")`.
6. Display category details at `/categories/<int:pk>/`.
7. Add `Article.category` as a `ForeignKey` and display articles for a category.
8. Add `Article.is_published` and mark recent published articles in the list.
9. Override the Django admin title/template.
10. Add GET search by article title at `/articles/?q=...`.
