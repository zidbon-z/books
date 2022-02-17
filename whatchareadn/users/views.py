from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

#class Login(View):
#
#    def get(self, request):
#        return render(request, 'users/authentication/login.html')

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            messages.success(request, ("There was an issue, try again"))
            return redirect('login')
        
    else:
        return render(request, 'registration/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully logged out!"))
    return redirect('main:index')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('main:index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form,})
