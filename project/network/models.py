from django.db import models

# Create your models here.
class ConnectionRequest(models.Model):
    
    sender = models.ForeignKey("Profile.Profile", on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey("Profile.Profile", on_delete=models.CASCADE, related_name = "reciever")
    state = models.CharField(max_length=255, choices=CONNECTION_STATES, default="Pending")
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (('sender', 'reciever'))
      
    def __str__(self):
        return f"{self.sender.full_name} --> {self.reciever.full_name}"