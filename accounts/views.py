from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from . import forms
from store.models import *


# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            instance = form.save(commit=False)
            instance.name = request.user
            instance.customer = request.user
            instance.save()
            return redirect('home')
=======
            
            return redirect('accounts:login')
>>>>>>> 27f118911aca704bb87409323351786b3ca256ff

    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            # Log in the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:

                return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    #if request.method == 'POST':
    logout(request)
    return redirect('store')


