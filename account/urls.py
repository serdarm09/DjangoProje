from django.urls import path
from . import views 

#/login
#/register
#/home
#/profil
#/settings
#/logout
#user_profile
##/destek
##/iletişim
##/profilesettings

urlpatterns = [
    path("", views.views_login,name="login"),
    path('login', views.views_login,name="login"),
    path('register', views.register, name='register'),
    path("home",views.home,name='home'),
    path("profil",views.profil,name = 'profil'), 
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path("settings",views.settings,name="settings"),
    path("logout/",views.views_logout,name="logout"),
    path("message/",views.message,name='message'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('bagis_istegi_gonder/<int:post_id>/', views.bagis_istegi_gonder, name='bagis_istegi_gonder'),   
    path('post-action/<int:post_id>/', views.post_action, name='post_action'),
    path('donations', views.donations, name='donations'),  
    path('map/', views.map_view, name='map'),
    path('biografi/', views.biografi, name='biografi'),
    path('istek_kabul/<int:id>/', views.istek_kabul, name = 'istek_kabul'),
    path('istek_red/<int:id>/', views.istek_red, name = 'istek_red'),

    path("get_all_conversations", views.get_all_conversations, name="get_all_conversations"),
    path("get_messages", views.get_messages, name="get_messages"),
    path("send_message", views.send_message, name="send_message"),
]
