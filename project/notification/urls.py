from django.urls import path
from notification.views import *

urlpatterns = [
    path('list/', NotificationView.as_view())
    ]
    
    