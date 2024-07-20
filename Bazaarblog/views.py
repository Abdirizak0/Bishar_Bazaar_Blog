from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import UserRegistrationForm, BlogPostForm

def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'Bazaarblog/home.html', {'posts': posts})

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

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your blog post was created successfully!')
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, "You can't edit this post.")
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your blog post was updated successfully!')
            return redirect('post_detail', pk=pk)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'Bazaarblog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, "You can't delete this post.")
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your blog post was deleted successfully!')
        return redirect('home')
    
    return render(request, 'Bazaarblog/delete_post.html', {'post': post})