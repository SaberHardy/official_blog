from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from blogapp.models import Post


def home(request):
    posts = Post.new_manager.all()
    context = {
        'posts': posts
    }
    return render(request, 'blogapp/home.html', context)


def single_post(request, post):
    post_single = get_object_or_404(Post, slug=post, status='published')

    context = {
        'post_single': post_single
    }
    return render(request, 'blogapp/single_post.html', context)

