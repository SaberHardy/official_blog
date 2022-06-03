from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Profile
from .tokens import account_activation_token
from .forms import UserRegisterForm, UserEditForm, UserProfileForm


# def login(request):
#     return render(request, 'registration/login.html')

@login_required
def avatar_get(request):
    user = User.objects.get(username=request.user)
    avatar = Profile.objects.filter(user=user)
    context = {
        'user': user,
        'avatar': avatar
    }
    return context


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'section': 'profile'})


def accounts_register(request):
    # if they registered do that
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():  # check the data if it is valid
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            }
            message = render_to_string('registration/account_activation_email.html', context)
            user.email_user(subject=subject, message=message)
            return HttpResponse('You successfully registered, and the activation sent')

    # if the user want to register show the form
    else:
        register_form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': register_form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        profile_form = UserProfileForm(
            request.POST, request.FILES,
            instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/update.html', context)


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        # disable the account from db
        user.is_active = False
        user.save()
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/delete_account.html')
