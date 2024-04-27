from django.shortcuts import render,redirect
from .models import person,comments,group
from django.utils import timezone


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
        # Formdan gelen hedef kitle değerlerini bir liste olarak al
        selected_groups = request.POST.getlist('group')

        # Hedef kitle değerlerini istediğimiz formatta düzenle
        formatted_groups = ', '.join(selected_groups)

        name = request.POST.get('name')
        comment = request.POST.get('comment')
            
        # Yeni yorum oluştururken düzenlenmiş hedef kitle değerlerini kullan
        new_comment = comments.objects.create(group=formatted_groups, name=name, comment=comment, dateTime=timezone.now())
        new_comment.save()
        
        return redirect('home')

    all_comments = comments.objects.all()
    all_groups = group.objects.all()
    return render(request, "home.html", {'comments': all_comments, 'groups': all_groups})




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
        selected_group = request.POST.get('group')
        
        # Eğer e-posta adresi zaten kayıtlıysa hata sayfasına yönlendir
        if person.objects.filter(mail=mail).exists():
            return render(request, 'registerError.html')

        # Yeni bir Person nesnesi oluştur ve kaydet
        new_person = person.objects.create(
            first_name=first_name,
            last_name=last_name,
            mail=mail,
            password=password,
            isActive=True
        )
        # Seçilen hedef kitleyi kayıtlı kullanıcıya ata
        if selected_group:
            new_person.group = selected_group
            new_person.save()

        return redirect('login')  # Kayıt işlemi tamamlandıktan sonra giriş sayfasına yönlendir
    else:
        groups = group.objects.all()
        return render(request, 'register.html', {'groups': groups})  # Kayıt formunu gösterirken grupları template'e gönder

