from django.shortcuts import render
from .models import BlogPost

def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})