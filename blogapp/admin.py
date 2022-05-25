from django.contrib import admin

from blogapp.models import Post


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug')


admin.site.register(Post, AuthorAdmin)
