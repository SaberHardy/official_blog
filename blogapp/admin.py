from django.contrib import admin
from blogapp import models
from blogapp.models import Post, Comment, Category
from mptt.admin import MPTTModelAdmin


@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'category', 'id')
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = ('id',)


# @admin.register(models.Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'name', 'email', 'date_commented', 'status')
#     list_filter = ('status', 'date_commented')
#     search_fields = ('name', 'email', 'content')


# admin.site.register(Post, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Comment, MPTTModelAdmin)
