from django.contrib import admin
from .models import person,comments,group

@admin.register(group)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("group_name",)

@admin.register(comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("name","dateTime","isActive",)
    list_filter = ("isActive",)
    list_editable = ("isActive",)
    
@admin.register(person)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("first_name","mail","isActive","last_name")
    list_filter = ("isActive",)
    list_editable = ("isActive",)
    search_fields = ("first_name",  "mail","last_name",)
    