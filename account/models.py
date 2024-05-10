from django.db import models
from django.contrib.auth.models import User
from django import forms


class Audience(models.Model):
    name = models.DateField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.name

        
class Comment(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan kullanıcı
    title = models.CharField(max_length=100)  # Yorum başlığı
    content = models.TextField()  # Yorum içeriği
    image = models.ImageField(upload_to="profile_images",null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi

    class Meta:
        ordering = ['-created_at']  # Yorumları oluşturulma tarihine göre sırala
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

class VerifyCompany(models.Model):
    CompanyName = models.CharField(max_length=35)
    image = models.ImageField(upload_to="VerifyCompany",null=True, blank=True, default='')
    