from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



# http:127.0.0.1:8000
# http:127.0.0.1:8000/login
# http:127.0.0.1:8000/home
# http:127.0.0.1:8000/home/donate
# http:127.0.0.1:8000/home/postshare
# http:127.0.0.1:8000/home/donatemap
# http:127.0.0.1:8000/home/profile 

urlpatterns = [   
    path("", views.login_,name="login_1"),
    path('login', views.login_,name="login_1"),
    path('register', views.register_, name='register_1'),
    path("home",views.home_,name='home_1'),
    path("profil",views.profil_,name = 'profil_1'),
    path("settings",views.settings_,name="settings_1"),
]