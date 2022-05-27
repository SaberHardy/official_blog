from django.urls import path
from blogapp import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:post>/', views.single_post, name='single_post'),
    path('category/<category>/', views.CategoryListView.as_view(), name='category'),
]
