from django.urls import path
from . import views 

urlpatterns = [
    path("", views.views_login,name="login"),
    path('login', views.views_login,name="login"),
    path('register', views.register, name='register'),
    path("home",views.home,name='home'),
    path("profil",views.profil,name = 'profil'),
    path("settings",views.settings,name="settings"),
    path("logout/",views.views_logout,name="logout"),
]
