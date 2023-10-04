from django.contrib import admin
from notification.models import *
# Register your models here.

admin.site.register(Notification)
admin.site.register(NotificationType)