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