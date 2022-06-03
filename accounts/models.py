from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='user/avatar.jpg')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
