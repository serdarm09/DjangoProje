from django.db import models
from django.contrib.auth.models import User,AbstractUser,Group,Permission


class Audience(models.Model):
    name = models.DateField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.name

class UserChange(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  # Örnek olarak 'custom_user_groups' olarak belirtilebilir
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  # Örnek olarak 'custom_user_permissions' olarak belirtilebilir
    )
class Comment(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan kullanıcı
    title = models.CharField(max_length=100)  # Yorum başlığı
    content = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi

    class Meta:
        ordering = ['-created_at']  # Yorumları oluşturulma tarihine göre sırala
