from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = "messaging"
urlpatterns = [   
    # path("", views.messaging, name="messaging"),
    path("get_all_conversations", views.get_all_conversations, name="get_all_conversations"),
    path("get_messages", views.get_messages, name="get_messages"),
    path("send_message", views.send_message, name="send_message"),
]