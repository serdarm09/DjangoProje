from django.shortcuts import render,redirect
from .models import person,comments
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

@login_required
def my_protected_view(request):
    # Kullanıcı giriş yapmışsa buraya erişebilir
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        if person.objects.filter(isActive = 1)==False:
            #kullanıcı aktif değilse mesajı fırlat
            return render(request, 'login.html', {'error_message': 'Kullanıcı Deaktif lütfen müşteri hizmetleriyle iletişime geçin'})
        elif person.objects.filter(mail=mail, password=password, isActive = 1).exists():
            # Kullanıcı mevcutsa oturumu başlat
            return redirect('home')  # Giriş başarılıysa ana sayfaya yönlendir
        else:
            # Kullanıcı mevcut değilse hata mesajı göster
            return render(request, 'login.html', {'error_message': 'Kullanıcı adı veya şifre yanlış'})
    else:
        # isteği ise boş bir formu göster
        return render(request, 'login.html')

def homes(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        # Yeni bir yorum oluştur
        new_comment = comments.objects.create(name=name, comment=comment)
        new_comment.save()  # Yorumu kaydet
        return redirect('home')  # PRG prensibi uygulanıyor
    all_comments = comments.objects.all()  # Tüm yorumları getir
    return render(request, "home.html", {'comments': all_comments})


def profile(request):
    return render(request,"profile.html")

def getDonationByCategory(request,category):
    if( category == "profile"):
        return render(request,"profile.html")
    else:
        return render(request,"error.html") 
    
def getDonationByCategoryId(request):
    return render(request,"error.html")

def register(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        if person.objects.filter(mail=mail).exists():
         # Eğer e-posta adresi zaten kayıtlı ise hata mesajı göster
            
            return render(request,'registerError.html')
            

        # Veritabanına yeni bir Person nesnesi oluştur
        new_person = person(first_name=first_name, last_name=last_name, mail=mail, password=password, isActive=True)
        new_person.save()

        return redirect('login')
    else:
        # GET isteği ise boş bir formu göster
        return render(request, 'register.html')