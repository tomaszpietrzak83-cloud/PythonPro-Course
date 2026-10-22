from django import forms

from .models import Genre, Tag, UserGame


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


class LibraryFilterForm(forms.Form):
    list_type = forms.ChoiceField(
        label="Collection",
        choices=[("all", "All games"), *UserGame.ListType.choices],
        required=False,
    )


class UserGameEditForm(forms.ModelForm):
    class Meta:
        model = UserGame
        fields = ("play_status", "rating", "note")
        labels = {"note": "Private note"}
        help_texts = {
            "rating": "Rate from 1 to 10, or leave blank.",
            "note": "Only you can see this note in your library (up to 5000 characters).",
        }
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
            "note": forms.Textarea(attrs={"rows": 5}),
        }
