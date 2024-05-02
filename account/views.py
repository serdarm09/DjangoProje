from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment
import random

def views_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Hatalı e-posta veya şifre"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def company(request):
    return(request,"error.html")

@login_required
def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        post_title = request.POST.get('post_title')
        post_content = request.POST.get('post_content')
        if post_content:  # Eğer içerik dolu ise
            # Yeni bir post oluştur ve veritabanına kaydet
            Comment.objects.create(user=request.user, title=post_title, content=post_content)
            # Post gönderildikten sonra ana sayfaya yönlendir
            return redirect('home')
        elif not post_title:
            error_message = "başlık olamdan olmaz reis"
            return render(request, 'index.html', {'error_message': error_message})
        else:
            # Eğer içerik boş ise, hata mesajı göster
            error_message = "Post içeriği boş olamaz."
            return render(request, 'index.html', {'error_message': error_message})
    else:
        # GET isteği alınırsa, post oluşturma formunu göster
        all_posts = Comment.objects.all()
        # Sayfalama
        paginator = Paginator(all_posts, 10) # Sayfa başına 10 post
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Eğer page sayısı bir integer değilse, ilk sayfayı getir
            posts = paginator.page(1)
        except EmptyPage:
            # Eğer page numarası sayfalama sınırlarının dışındaysa, son sayfayı getir
            posts = paginator.page(paginator.num_pages)
            
        return render(request, 'index.html',{'users': users, 'posts': posts})
   
    
    
@login_required
def settings(request):
    if request.method == 'POST':
        # Kullanıcı bilgilerini güncelle
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.username = request.POST.get('username')
        request.user.birth_date = request.POST.get('birth_date')
        request.user.email = request.POST.get('email')
        request.user.save()
  
        return redirect('home')  # Varsayılan olarak ana sayfaya yönlendir
    else:
        # GET isteği alınırsa, mevcut kullanıcı bilgilerini içeren bir form göster
        return render(request, 'settings.html')



def register(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Parola doğrulaması yap
        if password != confirm_password:
            error_message = "Parolalar eşleşmiyor."
            return render(request, 'register.html', {'error_message': error_message})
        #Mail kayıtlıysa hata yakalar
        if User.objects.filter(email=email).exists():
            error_message = "Bu kullanıcı maili sisteme kayıtlı."
            return render(request, 'register.html', {'error_message': error_message})
        
        if User.objects.filter(username=username).exists():
            error_message = "Bu Kullanıcı adı kullanılıyor"
            return render(request, 'register.html', {'error_message': error_message})
        
        # Kullanıcı oluştur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Kayıt başarılı olduğunda kullanıcıyı giriş yap sayfasına yönlendir
        return redirect('login')
    else:
        # GET isteği varsa, kayıt formunu göster
        return render(request, 'register.html')
    
@login_required
def profil(request):
    return render(request,"my-profile.html")

def views_logout(request):
    logout(request)
    return redirect("login")  
