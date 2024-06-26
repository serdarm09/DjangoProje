from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment,UserProfile,BagisIstegi,Biografi
from PIL import Image
from django.core.exceptions import ValidationError
from geopy.geocoders import Nominatim
import folium

from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import Message

import json


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
    
    user_biografi = Biografi.objects.filter(user=request.user).first()
    all_posts = Comment.objects.filter(comment_isactive=True,comment_succes=False)
    istekler = BagisIstegi.objects.filter(post__user=request.user, is_active = False)
    paginator = Paginator(all_posts, 10)
    
    page = request.GET.get('page')
    query = request.GET.get('q')
    
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'users': users, 'posts': posts, 'istekler': istekler, 'user_biografi': user_biografi})


@login_required
def istek_kabul(request, id):
    istek = get_object_or_404(BagisIstegi, id=id)
    # Kabul işlemleri burada yapıldı
    istek.is_active = True  # İsteği aktif yaparak kabul edilmiş olarak işaretleyin
    istek.save()
    return redirect('message')

@login_required
def istek_red(request, id):
    istek = get_object_or_404(BagisIstegi, id=id)
    istek.delete()  # İsteği reddederek silin
    return redirect('home')



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

def biografi(request):
    try:
        biografi = Biografi.objects.get(user=request.user)
    except Biografi.DoesNotExist:
        biografi = None
    
    if request.method == 'POST':
        bio_content = request.POST.get('bio')
        if biografi:
            biografi.bio = bio_content
        else:
            biografi = Biografi(user=request.user, bio=bio_content)
        biografi.save()
        return redirect('biografi')
    
    return render(request, 'settings.html', {'biografi': biografi})

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
        post_image = request.FILES.get("post_image")
        post_country = request.POST.get("post_country")
        post_city = request.POST.get('post_city')
        post_district = request.POST.get('post_district')
        
        if post_content:  # Eğer içerik dolu ise
            # Yeni bir post oluştur ve veritabanına kaydet
            Comment.objects.create(user=request.user, title=post_title, content=post_content, image=post_image, country = post_country ,city=post_city, district=post_district)
            # Post gönderildikten sonra ana sayfaya yönlendir
            return redirect('profil')
    # Kullanıcının oluşturduğu postları filtrele
    user_biografi = Biografi.objects.filter(user=request.user).first()
    comments = Comment.objects.filter(user__username=request.user, comment_isactive=True,comment_succes=False)
    user = User.objects
    
    # Şablonla kullanıcı postlarını gönder
    return render(request, "my-profile.html", {'user_posts': comments,'users_data':user ,"user_biografi":user_biografi}) 

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
    user_biografi = Biografi.objects.filter(user=request.user).first()
    user = User.objects
    
    # kullanıcı postlarını gönder  
    return render(request, 'donations.html', {'users':user,'user_posts': comments, 'users_data': user,"user_biografi":user_biografi})

@login_required
def message(request):
    
    istekler = BagisIstegi.objects.filter(post__user=request.user, is_active = True)
    
    return render(request,'messaging.html',{'istekler': istekler})


def views_logout(request):
    logout(request)
    return redirect("login")  


####################################
################MAP#################


def get_location(city, district, neighborhood):
    geolocator = Nominatim(user_agent="ac8ff2b6337c431bba6568c8ee221e55")
    location = geolocator.geocode(f"{neighborhood}, {district}, {city}, Turkey")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def show_on_map(locations):
    map_center = [39.9334, 32.8597]  # Ankara koordinatları merkezi göstersin diye
    my_map = folium.Map(location=map_center, zoom_start=6)
    
    for city, district, neighborhood, title, username in locations:
        lat, lon = get_location(city, district, neighborhood)
        if lat and lon:
            folium.Marker(
                location=[lat, lon],
                popup=f"{title} by {username}<br>{neighborhood}, {district}, {city}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(my_map)
        else:
            print(f"Location not found: {neighborhood}, {district}, {city}")
    
    return my_map


def map_view(request):
    comments = Comment.objects.filter(comment_isactive=True, comment_succes=False).values('city', 'country', 'district', 'title', 'user__username')
    locations = [(comment['city'], comment['country'], comment['district'], comment['title'], comment['user__username']) for comment in comments]
    my_map = show_on_map(locations)
    
    my_map.save("static/map1.html")
    
    users = User.objects.all()
    
    
    return render(request, 'map.html',{'user':users})


###  messaging views ### 



def get_all_conversations(request):

    all_messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by("-date")
    conversations = []
    usernames = []

    for message in all_messages:
        if message.receiver == request.user:
            if message.sender.username in usernames:
                continue
            pp = None
            try:
                pp = message.sender.userprofile.profile_picture.url
            except:
                pass
            data_to_append = {
                "user_id": message.sender.id, 
                "username": message.sender.username, 
                "date": message.date, 
                "message": message.message, 
                "istek": {
                    "user": {
                        "profilePic": pp,
                    },
                }
            }
            conversations.append(data_to_append)
            usernames.append(message.sender.username)
        else:
            if message.receiver.username in usernames:
                continue
            pp = None
            try:
                pp = message.receiver.userprofile.profile_picture.url
            except:
                pass
            data_to_append = {
                "user_id": message.receiver.id, 
                "username": message.receiver.username, 
                "date": message.date, 
                "message": message.message, 
                "istek": {
                    "user": {
                        "profilePic": pp,
                    },
                }
            }
            conversations.append(data_to_append)
            usernames.append(message.receiver.username)


    return JsonResponse({"conversations": conversations})


@csrf_exempt
def get_messages(request):

    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=400)

    user_id = request.POST.get("user_id", None)
    if user_id is None:
        return JsonResponse({"error": "user_id missing"}, status=400)
        
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"user with id {user_id} does not exist"}, status=400)

    received_messages = Message.objects.filter(Q(receiver=request.user) & Q(sender=other_user))
    sent_messages = Message.objects.filter(Q(receiver=other_user) & Q(sender=request.user)) 
    
    received_messages.update(is_read=True)  # mark received messages as read
    
    messages = received_messages | sent_messages
    messages = messages.order_by("date")


    istek_detaylari = {
        "title": messages.first().istek.post.title,
        "country": messages.first().istek.country,
        "city": messages.first().istek.city,
        "district": messages.first().istek.district,
    }

    messages_to_return = [
        {
            "is_sent": message.sender == request.user,
            "is_read": message.is_read,
            "message": message.message,
            "date": message.date,
        }
    for message in messages]
    
    return JsonResponse({"messages": messages_to_return, "istekDetaylari": istek_detaylari, "other_user": {"username": other_user.username, "last_login": other_user.last_login}})


@csrf_exempt
def send_message(request):

    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=400)

    user_id = request.POST.get("user_id", None)
    message = request.POST.get("message", None)

    if user_id is None:
        return JsonResponse({"error": "user_id is missing"}, status=400)
        
    if message is None:
        return JsonResponse({"error": "message is content missing"}, status=400)
    
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": f"user with id {user_id} does not exist"}, status=400)
    
    Message.objects.create(sender=request.user, receiver=other_user, message=message)

    return JsonResponse({"message": "successful"}, status=200)




