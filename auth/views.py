from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User

from auth import forms

# Create your views here.

# By default Logout redirect url shows default Django Administration Logout Page
class Logout(LogoutView):
    next_page = '/'

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    loginForm = forms.LoginForm()
    error = None
    if request.method == 'POST':
        loginForm = forms.LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user:
                # creates session for user in request variable
                auth_login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect('/')
            else:
                error = 'Invalid username or password'
    context = {
        "form": loginForm,
        "error": error
    }
    return render(request, 'auth/login.html', context)

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    registerForm = forms.RegisterForm()
    addressForm = forms.AddressForm()
    error = None
    if request.method == 'POST':
        registerForm = forms.RegisterForm(request.POST)
        addressForm = forms.AddressForm(request.POST)
        if registerForm.is_valid():
            user = None
            try:
                username = registerForm.cleaned_data['username']
                email = registerForm.cleaned_data['email']
                password = registerForm.cleaned_data['password']
                first_name = registerForm.cleaned_data['first_name']
                last_name = registerForm.cleaned_data['last_name']
            except Exception as e:
                print(e)
            try:
                User.objects.get(username = username)
                # User exists if execution reaches here
                # as no error occured in accessing user
                error = "User already exists"
            except User.DoesNotExist:
                try:
                    user = User.objects.create_user(username = username, password = password, email = email,first_name = first_name, last_name = last_name)
                    # User created successfully if execution reaches here
                    # as no error occured in creating user
                except:
                    # user could not be created
                    user = None
                if user:
                    # store other user details in database
                    register = registerForm.save()
                    address = addressForm.save()
                    register.address = address
                    register.save()
                    return HttpResponseRedirect('/auth/login')
                else:
                    error = "User could not be created"
    context = {
        "form": registerForm,
        "addressform": addressForm,
        "error": error
    }
    return render(request, 'auth/register.html', context)
