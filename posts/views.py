from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    
    post = Post.objects.all().order_by('-id')
    comment_form = CommentForm()

    context = {
        'posts' : post,
        'comment_form': comment_form,
    }
    
    return render(request, 'index.html', context)
    
@login_required
def create(request):
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
        
    else:
        form = PostForm()
        
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)

@login_required
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)

        comment.user = request.user

        post = Post.objects.get(id=post_id)
        comment.post = post

        comment.save()

        return redirect('posts:index')
    
@login_required
def like(request, post_id):
    
    user= request.user
    post= Post.objects.get(id=post_id)
    
    if user in post.like_users.all():
        post.like_users.remove(user)
        
    else:
        post.like_users.add(user)
        
    return redirect('posts:index')