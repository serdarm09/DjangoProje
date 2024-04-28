from django.urls import path
from . import views 
urlpatterns = [
    path("login",views.login_request, name='login_1'),
    path("register",views.register_request, name='register_1'),
    path("logout",views.logout_request, name='logout_1'),
    path("profile",views.profile_request, name='profile_1'),
    path("home",views.home_views, name='home_1'),
]
