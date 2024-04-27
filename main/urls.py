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
     path("", views.login),
     path("register",views.register),
     path('register/', views.register, name='register'),
     path('login', views.login, name='login'),
     path("home",views.homes,name='home'),
     path("profile",views.profile,name='profile')
     # path("<int:category_id>",views.getDonationByCategoryId),
     # path("<str:category>",views.getDonationByCategory)
]