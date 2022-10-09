from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


# User = settings.AUTH_USER_MODEL


def user_directory_path(instance, filename):
    # return 'posts/%Y/%m/%d/'.format(instance.id, filename)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', null=True, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    favorites = models.ManyToManyField(User, related_name='favorite', default=None, blank=True)

    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    thumbs = models.ManyToManyField(User, related_name='thumbs', default=None, blank=True)
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')

    image = models.ImageField(upload_to=user_directory_path, default='posts/trees.jpeg')

    # instead of using everytime the order we need to make it by default
    objects = models.Manager()  # default manager
    new_manager = NewManager()  # custom manager

    class Meta:
        # add "-" showing the last one added (by newer post)
        ordering = ['-publish', ]

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     else:
    #         self.slug = slugify(self.slug)
    #
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:home')

    # we can use this instead of signals in this case

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Post, self).save(*args, **kwargs)


class Comment(MPTTModel):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE, default=None, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    # name = models.CharField(max_length=50)
    # email = models.EmailField()
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    # we don't need this meta class
    # class Meta:
    #     # add "-" showing the last one added (by newer post)
    #     ordering = ('date_commented',)

    class MPTTMeta:
        order_insertion_by = ['date_commented']

    # def __str__(self):
    #     return f"Comment by {self.name}"


class Vote(models.Model):
    post = models.ForeignKey(Post, related_name='postid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)
