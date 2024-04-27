from django.db import models
from django.utils import timezone

class group(models.Model): 
    group_name = models.CharField(max_length=60)


class person(models.Model):  
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=40)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    isActive = models.BooleanField()
    group = models.CharField(max_length=40)


class comments(models.Model):  
    group = models.CharField(max_length=100)
    name = models.CharField(max_length=35)
    comment = models.TextField()
    dateTime = models.DateTimeField(default=timezone.now)
    isActive = models.BooleanField(default=True)

    