from django.contrib.auth import get_user_model
from django.db import models

from tinder.base.services import get_path_upload_avatar

UserModel = get_user_model()


class Client(UserModel):
    avatar = models.ImageField(upload_to=get_path_upload_avatar, blank=True, null=True)
    gender_choices = [
        ('M', 'Man'),
        ('W', 'Woman'),
    ]
    gender = models.CharField(max_length=2, choices=gender_choices)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.username
