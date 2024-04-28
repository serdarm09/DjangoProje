from django.shortcuts import render
from .models import models

def login_request(request):
    return render(request,"account/login.html")

def register_request(request):
    return render(request,"account/register.html")

def logout_request(request):
    return render(request,"logout.html")
