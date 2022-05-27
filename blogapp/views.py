from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from blogapp.forms import CommentForm
from blogapp.models import Post


def home(request):
    posts = Post.new_manager.all()
    context = {
        'posts': posts
    }
    return render(request, 'blogapp/home.html', context)


def single_post(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    comments = post.comments.filter(status=True)
    user_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'comment_form': comment_form,
        'post': post,
        'comments': comments,
        'user_comment': user_comment,
    }
    return render(request, 'blogapp/single_post.html', context)
