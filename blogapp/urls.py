from django.urls import path
from blogapp import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('createpost/', views.CreatePostView.as_view(), name='createpost'),
    path('search/', views.post_search, name='search'),
    path('addcomment/', views.add_comment, name='addcomment'),
    path('<int:pk>/', views.single_post, name='single_post'),
    path('category/<category>/', views.CategoryListView.as_view(), name='category'),

]
