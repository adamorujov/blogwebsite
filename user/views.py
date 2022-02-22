from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from user.forms import RegisterForm, LoginForm
from user.models import CustomUser
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def signUser(request):
    if request.user.is_authenticated:
        raise Http404

    elif request.POST.get("choice") == "signin":
        username = request.POST.get("username1")
        password = request.POST.get("password1")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Username or password is incorrect")
            return render(request, 'signin.html')

        messages.success(request, "Welcome, %s" % username)
        login(request, user)

        if request.POST.get("check"):
            request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
            
        return redirect("index")

    elif request.POST.get("choice") == "signup":
        username = request.POST.get("username2")
        email = request.POST.get("email")
        password1 = request.POST.get("password2")
        password2 = request.POST.get("password3")

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, "Please, choose another username.")
            return redirect("user:login")

        elif password1 != password2:
            messages.info(request, "Passwords do not match.")
            return redirect("user:login")

        user = CustomUser(username=username, email=email)
        user.set_password(password1)
        user.save()
        login(request, user)
        messages.success(request, "%s, you successfully signed up." % username)
        return redirect("index")

    return render(request, 'signin.html')

def logoutUser(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("index")

