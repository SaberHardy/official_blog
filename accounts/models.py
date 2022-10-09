from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='user/avatar.jpg')
    bio = models.TextField(max_length=500, blank=True)

    # we limit the size of user image
    def clean(self):
        if not self.avatar:
            raise ValueError("x")
        else:
            w, h = get_image_dimensions(self.avatar)
            if w >= 200:
                raise ValidationError('x')
            if h >= 200:
                raise ValidationError('x')

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # after created the new user will link it to profile
#         print("Profile has been created!!!")
#         Profile.objects.create(user=instance)
