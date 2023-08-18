from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm, SignInForm
from django.shortcuts import redirect, render





def signup(request):
    if request.method == 'POST':
        form_signup = SignUpForm(request.POST)
        if form_signup.is_valid():
            user = form_signup.save()
            return redirect('signin')
    else:
        form_signup = SignUpForm()
  
    title = "Sign Up"
    context = {
        'title': title,
        'form_signup': form_signup,
    }
    return render(request, 'accounts/signup.html', context)


def signin(request):
    if request.method == 'POST':
        form_signin = SignInForm(request.POST)
        if form_signin.is_valid():
            username = form_signin.cleaned_data['username']
            password = form_signin.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form_signin = SignInForm()

    title = "Sign In"
    context = {
        'title': title,
        'form_signin': form_signin,
    }
    return render(request, 'accounts/signin.html', context)


def logout_user(request):
    logout(request)
    return redirect('')