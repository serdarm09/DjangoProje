from typing import Any
from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan kullanıcı
    title = models.CharField(max_length=100)  # Yorum başlığı
    content = models.TextField()  # Yorum içeriği
    image = models.ImageField(upload_to="profile_images", null=True, blank=True)  # Resim alanı
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi
    comment_isactive = models.BooleanField(default=True)  # Yorumun aktif olup olmadığını belirten alan
    comment_succes = models.BooleanField(default=False)  # Yorumun başarılı olup olmadığını belirten alan
    country = models.CharField(max_length=100)  # Ülke bilgisi
    city = models.CharField(max_length=100)  # Şehir bilgisi
    district = models.CharField(max_length=100, blank=True, null=True)  # İlçe bilgisi, boş ve null olabilir

    class Meta:
        ordering = ['-created_at']  # Yorumları oluşturulma tarihine göre sırala


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True,default='')
    
class Biografi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()

class VerifyCompany(models.Model):
    CompanyName = models.CharField(max_length=35)
    image = models.ImageField(upload_to="VerifyCompany",null=True, blank=True, default='')


class BagisIstegi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)
    istek_mesaji = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
    
    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            Message.objects.create(
                sender=self.user,
                receiver=self.post.user,
                message=self.istek_mesaji,
                istek=self
            )
            
    

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    istek = models.ForeignKey(BagisIstegi, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='message_image', blank=True, null=True,default='')

    def __str__(self) -> str:
        return f"{self.sender.username} to {self.receiver.username} at {self.date}"
