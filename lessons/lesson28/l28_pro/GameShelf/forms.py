from django import forms

from .models import Genre


class CatalogFilterForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(), to_field_name="slug", required=False,
        empty_label="All genres",
    )
