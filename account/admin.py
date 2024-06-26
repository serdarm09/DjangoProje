from django.contrib import admin
from .models import Comment, Message, BagisIstegi

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("title","content",)

admin.site.register(Message)
admin.site.register(BagisIstegi)

