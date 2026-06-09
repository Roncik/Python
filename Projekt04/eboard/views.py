from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Post, Comment
from .forms import RegistrationForm, PostForm, CommentForm

def home(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(location__icontains=search_query) |  Q(description__icontains=search_query)
        ).order_by('-date_posted')
    else:
        posts = Post.objects.all().order_by('-date_posted')
    
    return render(request, 'eboard/index.html', {'posts': posts, 'search_query': search_query})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'eboard/register.html', {'form': form, 'title': 'Register'})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'eboard/create_post.html', {'form': form, 'title': 'New post', 'legend': 'New post'})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You need to login to comment.')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post-detail', post_id=post.id)
    return render(request, 'eboard/post.html', {'title': post.title, 'post': post, 'form': form})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post-detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'eboard/create_post.html', {'title': 'Update Post', 'form': form, 'legend': 'Update Post'})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('home')
    return redirect('post-detail', post_id=post.id)

@login_required
def myposts(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(
            author=request.user
        ).filter(
            Q(title__icontains=search_query) | Q(location__icontains=search_query) |  Q(description__icontains=search_query)
        ).order_by('-date_posted')
    else:
        posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'eboard/my_posts.html', {'posts': posts, 'search_query': search_query})

@login_required
def mycomments(request):
    comments = Comment.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'eboard/my_comments.html', {'comments': comments})

# Obsługa błędów w widokach (wymaga DEBUG=False)
def handler404(request, exception):
    return render(request, 'eboard/404.html', status=404)

def handler500(request):
    return render(request, 'eboard/500.html', status=500)