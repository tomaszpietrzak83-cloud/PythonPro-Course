from django import forms

from .models import Genre, Tag


class CatalogFilterForm(forms.Form):
    q = forms.CharField(
        label="Search games",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type a game title...",
                "autocomplete": "off",
                "aria-controls": "search-suggestions",
                "aria-describedby": "search-status",
            }
        ),
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        to_field_name="slug",
        required=False,
        empty_label="All tags",
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        to_field_name="slug",
        required=False,
        empty_label="All genres",
    )
