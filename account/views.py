from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment,UserProfile,BagisIstegi
from PIL import Image
from django.core.exceptions import ValidationError



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
            messages = "Hatalı e-posta veya şifre"
            return render(request, 'login.html', {'messages': messages})
    return render(request, 'login.html')




@login_required
def validate_image(image):
    # Eğer resim yüklenmişse
    if image:
        # Dosya türünü kontrol et
        if not image.content_type.startswith('image'):
            raise ValidationError("Geçersiz dosya türü: Sadece resim dosyaları desteklenmektedir.")
        # Resmin geçerliliğini kontrol et
        try:
            img = Image.open(image)
            img.verify()  # Resim dosyasını doğrula
        except Exception as e:
            raise ValidationError("Geçersiz resim dosyası: {}".format(e))

@login_required
def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        post_title = request.POST.get('post_title')
        post_content = request.POST.get('post_content')
        post_image = request.FILES.get("post_image")
        post_country = request.POST.get("post_country")
        post_city = request.POST.get('post_city')
        post_district = request.POST.get('post_district')
        
        if post_content:
            Comment.objects.create(user=request.user, title=post_title, content=post_content, image=post_image, country = post_country ,city=post_city, district=post_district)
            return redirect('home')
        else:
            return render(request, 'error.html')

    all_posts = Comment.objects.filter(comment_isactive=True,comment_succes=False)
    istekler = BagisIstegi.objects.filter(post__user=request.user)
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'users': users, 'posts': posts, 'istekler': istekler})

@login_required
def post_action(request, post_id):
    post = get_object_or_404(Comment, id=post_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            post.comment_isactive = False
            post.save()
        elif action == 'success':
            post.comment_succes = True
            post.save()
    return redirect('home')


@login_required
def bagis_istegi_gonder(request, post_id):
    if request.method == 'POST':
        istek_mesaji = request.POST.get('istek_mesaji')
        country = request.POST.get('country')
        city = request.POST.get('city')
        district = request.POST.get('district')
        post = get_object_or_404(Comment, pk=post_id)
        
        
        #Bağış isteği verilerini kaydet
        BagisIstegi.objects.create(user=request.user, post=post, istek_mesaji=istek_mesaji, country=country, city=city, district=district)
        #Kullanıcıya mesaj göster
        return redirect('home')
    else:
        return redirect('home')  # GET isteklerine karşı doğrudan ana sayfaya yönlendiriyoruz



@login_required
def profile_settings(request):
    
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        
    if request.method == 'POST':
        user_profile.profile_picture = request.FILES.get('profile_picture')
        user_profile.birth_date = request.POST.get('birth_date')
        if(user_profile.birth_date):
            # UserProfile nesnesini kaydet
            user_profile.save()
            return redirect('home')
        else:
            error_message = "Parolalar eşleşmiyor"
            return render(request,"error.html",  {'error_message': error_message})
    else:
        # GET isteği alınırsa, mevcut kullanıcı bilgilerini içeren bir form göster
        return render(request, 'settings.html')



@login_required
def settings(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        # Kullanıcı bilgilerini güncelle
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        # Doğum tarihini ve profil resmini güncelle

        # UserProfile nesnesini kaydet
        user_profile.save()

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
    if request.method == 'POST':
        post_title = request.POST.get('post_title')
        post_content = request.POST.get('post_content')
        post_image = request.FILES.get('post_image')
        if post_content:  # Eğer içerik dolu ise
            # Yeni bir post oluştur ve veritabanına kaydet
            Comment.objects.create(user=request.user, title=post_title, content=post_content, image=post_image)
            # Post gönderildikten sonra ana sayfaya yönlendir
            return redirect('profil')
    # Kullanıcının oluşturduğu postları filtrele
    comments = Comment.objects.filter(user__username=request.user, comment_isactive=True)
    user = User.objects
    
    # Şablonla kullanıcı postlarını gönder
    return render(request, "my-profile.html", {'user_posts': comments,'users_data':user}) 

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Comment.objects.filter(user=user,comment_succes=False, comment_isactive=True)
    
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    return render(request, 'user-profile.html', {'profile_user': user, 'user_posts': user_posts, 'user_profile': user_profile})

@login_required
def donations(request):
    # Yalnızca başarılı olan kullanıcı postlarını filtrele
    comments = Comment.objects.filter(user__username=request.user.username, comment_succes=True, comment_isactive=True)
    user = User.objects.all()
    
    # Şablonla kullanıcı postlarını gönder  
    return render(request, 'donations.html', {'user_posts': comments, 'users_data': user})

@login_required
def message(request):
    return render(request,'messaging.html')


def company(request):
    return render(request,"Company.html")


def views_logout(request):
    logout(request)
    return redirect("login")  
