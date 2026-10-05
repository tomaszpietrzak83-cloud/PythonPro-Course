from django import forms

from .models import Genre, Tag


class CatalogFilterForm(forms.Form):
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(), to_field_name="slug", required=False,
        empty_label="All tags",
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(), to_field_name="slug", required=False,
        empty_label="All genres",
    )
