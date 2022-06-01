from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# def login(request):
#     return render(request, 'registration/login.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'section': 'profile'})
