from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from blogapp.models import Post


@receiver(post_save, sender=Post)
def slugify_title_model_field(sender, instance, created, **kwargs):
    if created:
        post_to_slugify = Post.objects.get(id=instance.id)
        post_to_slugify.title = slugify(post_to_slugify.title)
        post_to_slugify.slug = slugify(post_to_slugify.title)
        post_to_slugify.save()
