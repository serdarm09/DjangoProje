from django.db import models
from django.utils import timezone

#veri tabanı modulleri burada oluşturulur.
class person(models.Model):
    first_name = models.CharField(max_length=35)
    last_name  = models.CharField(max_length=40)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    isActive = models.BooleanField()
    
    def __str__(self):
        return f"{self.first_name} {self.mail} {self.password}"
    
class comments(models.Model):
    name = models.CharField(max_length=35)
    comment = models.TextField() 
    dateTime = models.DateTimeField(default=timezone.now)  # Kullanıcı tarafından belirtilmeyen durumlarda şu anki tarihi ve saati alır
    isActive = models.BooleanField(default=True)  # Yorumun varsayılan olarak etkin olduğunu varsayalım
    

    