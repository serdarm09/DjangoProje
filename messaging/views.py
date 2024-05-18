from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Message  # , Conversation

import json


def get_all_conversations(request):

    all_messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by("-date")
    conversations = []
    usernames = []

    for message in all_messages:
        if message.receiver == request.user:
            if message.sender.username in usernames:
                continue

            data_to_append = {
                "user_id": message.sender.id, 
                "username": message.sender.username, 
                "date": message.date, 
                "message": message.message, 
            }
            conversations.append(data_to_append)
            usernames.append(message.sender.username)
        else:
            if message.receiver.username in usernames:
                continue

            data_to_append = {
                "user_id": message.receiver.id, 
                "username": message.receiver.username, 
                "date": message.date, 
                "message": message.message, 
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

    messages_to_return = [
        {
            "is_sent": message.sender == request.user,
            "is_read": message.is_read,
            "message": message.message,
            "date": message.date,
        }
    for message in messages]
    
    return JsonResponse({"messages": messages_to_return, "other_user": {"username": other_user.username, "last_login": other_user.last_login}})


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




