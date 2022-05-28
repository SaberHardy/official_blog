from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from django.db import models


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    # models.PROTECT will allow us to keep our post in our database
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=2)
    excerpt = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    image = models.ImageField(upload_to=user_directory_path, default='posts/trees.jpeg')

    # instead of using everytime the order we need to make it by default
    objects = models.Manager()  # default manager
    new_manager = NewManager()  # custom manager

    class Meta:
        # add "-" showing the last one added (by newer post)
        ordering = ['-publish', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:single_post', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        # add "-" showing the last one added (by newer post)
        ordering = ('date_commented',)

    def __str__(self):
        return f"Comment by {self.name}"
