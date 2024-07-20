
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost, Comment
from .forms import UserRegistrationForm, BlogPostForm, CommentForm
from django.core.paginator import Paginator
from django.shortcuts import render

def home(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'Bazaarblog/home.html', {'posts': posts, 'categories': categories})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your blog post was created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'Bazaarblog/create_post.html', {'form': form})

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = BlogPost.objects.filter(category=category).order_by('-created_at')
    return render(request, 'Bazaarblog/category_posts.html', {'category': category, 'posts': posts})


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

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment was added successfully!')
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'Bazaarblog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        posts = BlogPost.objects.all()
    
    context = {
        'posts': posts,
        'query': query
    }
    return render(request, 'Bazaarblog/search_results.html', context)