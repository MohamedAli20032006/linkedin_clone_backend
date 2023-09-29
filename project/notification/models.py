from django.db import models

# Create your models here.
class NotificationType(models.Model):
    
    type = models.CharField(max_length=100)