from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models


class Post(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')

    # instead of using everytime the order we need to make it by default
    objects = models.Manager()  # default manager
    new_manager = NewManager()  # custom manager

    class Meta:
        # add "-" showing the last one added (by newer post)
        ordering = ['-publish', ]

    def __str__(self):
        return self.title


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
