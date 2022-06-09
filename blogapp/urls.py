from django.urls import path
from blogapp import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.post_search, name='search'),
    path('addcomment/', views.add_comment, name='addcomment'),
    path('<slug:post>/', views.single_post, name='single_post'),
    path('category/<category>/', views.CategoryListView.as_view(), name='category'),

]
