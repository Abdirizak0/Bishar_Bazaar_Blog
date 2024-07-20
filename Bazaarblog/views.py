 #Bazaarblog/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import BlogPost
from .forms import UserRegistrationForm

def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})