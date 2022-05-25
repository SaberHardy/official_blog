from django.http import HttpResponse
from django.shortcuts import render

from blogapp.models import Post


def home(request):
    posts = Post.new_manager.all()
    context = {
        'posts': posts
    }
    return render(request, 'blogapp/index.html', context)
