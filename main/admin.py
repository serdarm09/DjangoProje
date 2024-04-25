from django.contrib import admin
from .models import person,comments

@admin.register(comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("name","dateTime","isActive",)
    
@admin.register(person)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("first_name","mail","isActive",)
    