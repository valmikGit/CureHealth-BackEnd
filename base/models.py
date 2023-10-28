from django.db import models
from healthcare.models import NewUser

# Create your models here.
class RoomMember(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200, verbose_name="Room Name")

    def save(self, *args, **kwargs):
        self.name = self.name
        super(RoomMember, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name