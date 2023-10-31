from django.db import models
from healthcare.models import NewUser

class OTP(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name='OTP_user')
    otp_secret = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
