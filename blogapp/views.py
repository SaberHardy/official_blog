from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blogapp.forms import CommentForm
from blogapp.models import Post, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    posts = Post.new_manager.all()
    context = {
        'posts': posts
    }
    return render(request, 'blogapp/home.html', context)


def single_post(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(allcomments, 2)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

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
        'allcomments': allcomments,
    }
    return render(request, 'blogapp/single_post.html', context)


class CategoryListView(ListView):
    template_name = 'blogapp/category.html'
    context_object_name = 'categorylist'

    def get_queryset(self):
        content = {
            'category': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']
                                         ).filter(status='published')
        }
        return content


def category_list(request):
    categories = Category.objects.exclude(name='default')
    context = {
        'categories': categories,
    }
    return context
