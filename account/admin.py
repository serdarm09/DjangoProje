from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("title","content",)