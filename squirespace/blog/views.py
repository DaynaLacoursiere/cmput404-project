from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic import FormView
from .models import Post, User
from .forms import PostForm, CommentForm, UserRegForm
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.http import HttpResponse
from friendship.models import Friend, Follow



class UserRegPage(FormView):
    template_name='blog/user_signup.html'
    success_url='/reg/confirm/'
    form_class = UserRegForm
    

def user_registration(request):
    print("FUCK",request.method)
    if request.method == "POST":
        form=UserRegForm(request.POST)
        if form.is_valid():                 # This never succeeds because we never call this view with a post.
            username = form.cleaned_data['username']
            email=form.cleaned_data['email']
            password= form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)  #THIS ABSOLUTELY DOES CREATE A USER. WE JUST NEED TO FIX EVERYTHING AROUND IT.
            user.save()
            return HttpResponse("/")
        else:
            print('Form validation failed.')
    else:
        form=UserRegForm()
        print('Blank form happened.')
    return render(request, 'registration/register_success.html', {'form':form})

def friends(request):
    return render(request, 'blog/friends.html')

def login(request):
    form = PostForm()
    return render(request, 'blog/login.html', {'form': form})

""" garbage
def image(request):
    image_data = open("../media/dnd.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
"""

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_with_comments.html', {'form': form,'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'post':post,'edit':True})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

def send_friend_request(request, pk):
    other_user = User.objects.get(pk = 1)
    Friend.objects.add_friend(request.user, other_user, message = 'I would like to request your friendship.')









