from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_request(request):
    if request.user.is_authenticated:
        return redirect("login_1")
    if request.method == 'POST':
        name = request.POST.get('mail')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            # Giriş başarılı olduğunda yapılacak işlemler
            return redirect("home_1")  # Örnek bir yönlendirme
        else:
            error_message = "Hatalı e-posta veya şifre"
            return render(request, 'login_1.html', {'error_message': error_message})
    return render(request, 'login_1.html')

def home_views(request):
    return render(request, "home_1.html")

def register_request(request):
    return render(request, "register_1.html")

def profile_request(request):
    return render(request,"profile_1.html")

def logout_request(request):
    logout(request)
    return redirect("login_1")  
