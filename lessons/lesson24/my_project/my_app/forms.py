from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# TASK 06
class RegistryForm(UserCreationForm):
    # TASK 06
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # TASK 06
        fields = ("username", "email", "password1", "password2")

    # TASK 06
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
