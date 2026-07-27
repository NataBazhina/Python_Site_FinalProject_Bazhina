from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = User.objects.get(username=username)
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})
