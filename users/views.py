from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from users.forms import UserRegistrationForm


def user_logout(request):
    '''for logout'''
    logout(request)
    return redirect("main")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('main')  # Redirect to the home page
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main")  # Redirect to homepage or dashboard
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})
