from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PWSResetForm, PwdResetConfirmForm, PassChangeForm

app_name = 'accounts'

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             authentication_form=UserLoginForm),
         name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html', form_class=PassChangeForm),
         name='password_change'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html', form_class=PWSResetForm),
         name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', form_class=PwdResetConfirmForm),
         name="pwdresetconfirm"),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),

    path('fav/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('profile/favorite_list/', views.favorite_list, name='favorite_list'),
    path('like/', views.like, name='like'),

    path('register/', views.accounts_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
