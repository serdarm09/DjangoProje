from django.db import models
from django.contrib.auth.models import User


class Audience(models.Model):
    name = models.DateField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.name

class UserChange(User):
    birth_date = models.CharField(max_length=100)
    
class Comment(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan kullanıcı
    title = models.CharField(max_length=100)  # Yorum başlığı
    content = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi

    class Meta:
        ordering = ['-created_at']  # Yorumları oluşturulma tarihine göre sırala




