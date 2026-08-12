from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import RegistryForm


# TASK 07
class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.get_user().username
        messages.success(self.request, f"Welcome back, {username}!")
        return response


# TASK 02
class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(request, "You have been logged out.")

        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            return HttpResponseRedirect(redirect_to)

        return super().get(request, *args, **kwargs)


# TASK 05
@login_required
def home(request):
    return render(request, "home.html")


# TASK 06 09
def register(request):
    if request.method == "POST":
        # TASK 06
        form = RegistryForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            # TASK 09
            auth_login(request, user)

            # TASK 04
            messages.success(
                request,
                f"Account for {username} was created! You can now logged in.",
            )

            return redirect("profile")
    else:
        # TASK 06
        form = RegistryForm()

    return render(request, "users/register.html", {"form": form})


# TASK 03
@login_required
def profile(request):
    return render(request, "users/profile.html")


# TASK 10
@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})
