from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def login_index(request):
    status = request.GET.get("status") or None
    data = {"status":status}
    return render(request, "login/index.html", context=data)

def login_auth(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.last_name == '100':
                return redirect("control_index")
            elif user.last_name == '200':
                return redirect("reception_index")
            elif user.last_name == '300':
                return redirect("security_index")
            elif user.last_name == '400':
                return redirect("control_index")
        return redirect("/login/?status=404")
    return redirect("login_index")

def login_logout(request):
    auth.logout(request)
    return redirect("login_index")