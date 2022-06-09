from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blogapp.forms import CommentForm, SearchForm
from blogapp.models import Post, Category, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def home(request):
    posts = Post.new_manager.all()
    context = {
        'posts': posts
    }
    return render(request, 'blogapp/home.html', context)


def single_post(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    favorite = bool
    if post.favorites.filter(id=request.user.id).exists():
        favorite = True

    allcomments = post.comments.filter(status=True)

    # page = request.GET.get('page', 1)
    # paginator = Paginator(allcomments, 2)
    # try:
    #     comments = paginator.page(page)
    # except PageNotAnInteger:
    #     comments = paginator.page(1)
    # except EmptyPage:
    #     comments = paginator.page(paginator.num_pages)
    #
    # user_comment = None
    #
    # if request.method == 'POST':
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         user_comment = comment_form.save(commit=False)
    #         user_comment.post = post
    #         user_comment.save()
    #         return HttpResponseRedirect('/' + post.slug)
    # else:
    #     comment_form = CommentForm()

    comment_form = CommentForm()

    context = {
        'comment_form': comment_form,
        'post': post,
        # 'comments': comments,
        # 'user_comment': user_comment,
        'allcomments': allcomments,
        'favorite': favorite,
    }
    return render(request, 'blogapp/single_post.html', context)


def add_comment(request):
    """
    Will capture the Ajax requests, when we create new comment that will going to
    create new ajax request and sent to this view and capture it using the if request.method == post
    """
    if request.method == "POST":

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})

        else:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.author = request.user
                user_comment.save()

                result = comment_form.cleaned_data.get('content')
                user = request.user.username

                return JsonResponse({'result': result, 'user': user})


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


# def post_search(request):
#     form = SearchForm()
#     q = ''
#     # c = ''
#     results = []
#     query = Q()
#
#     # this is caption the data that sent from ajax request
#     if request.POST.get('action') == 'post':
#         search_string = str(request.POST.get('ss'))
#
#         if search_string is not None:
#             search_string = Post.objects.filter(title__contains=search_string)[:3]
#             # As we know Javascript and python they can't talk to each others,
#             # so we need to serialize the data the gets return from database
#             data = serializers.serialize('json',
#                                          list(search_string),
#                                          fields=('id', 'title', 'slug'))
#
#             return JsonResponse({'search_string': data})
#
#     if 'q' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             q = form.cleaned_data['q']
#             # c = form.cleaned_data['categories']
#             #
#             # if c is not None:
#             #     query &= Q(category=c)
#             if q != '':
#                 query &= Q(title__contains=q)
#
#             results = Post.objects.filter(query)
#
#     context = {'form': form, 'q': q, 'results': results}
#     return render(request, 'blogapp/search.html', context)


def post_search(request):
    form = SearchForm()
    q = ''
    results = []

    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']

            # results = Post.objects.filter(title__search=q)

            # results = Post.objects.annotate(search=SearchVector(
            #     'title', 'content'),).filter(search=q)

            # results = Post.objects.annotate(search=SearchVector(
            #         'title', 'content'),).filter(search=SearchQuery(q))

            vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
            query = SearchQuery('q')

            results = Post.objects.annotate(
                rank=SearchRank(vector, query, cover_density=True)) \
                .order_by('-rank')

    context = {'form': form, 'q': q, 'results': results}
    return render(request, 'blogapp/search.html', context)
