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


class Match(models.Model):
    owner = models.ForeignKey(Client, related_name='match_owner', on_delete=models.CASCADE, blank=True, null=True)
    handpicked = models.ForeignKey(Client, related_name='match_handpicked', on_delete=models.CASCADE, blank=True,
                                   null=True)
    like = models.BooleanField()

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matchs"

    def __str__(self):
        return f'{self.owner.username} - {self.handpicked.username}'
