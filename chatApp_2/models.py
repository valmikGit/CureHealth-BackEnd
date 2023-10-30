from django.db import models
from healthcare.models import NewUser

# Create your models here.
class ChatMessage(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name="receiver")
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Messages"
    
    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver}"
    