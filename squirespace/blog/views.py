from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from .models import Post, User
from .forms import PostForm, CommentForm, UserRegForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from friendship.models import Friend, Follow, FriendshipRequest
from django.template.context_processors import csrf


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reg/confirm')
    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/user_signup.html', token)

def registration_complete(request):
    return render_to_response('registration/register_success.html')

def friends(request):
    return render(request, 'blog/friends.html')

def login(request):
    form = PostForm()
    return render(request, 'blog/login.html', {'form': form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    if (request.user.is_anonymous()):
        friends = []
    else:
        friends = Friend.objects.friends(request.user)
    return render(request, 'blog/post_list.html', {'posts': posts, 'friends': friends})

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


def profile(request,pk):
    profile_owner = User.objects.get(id=pk)
    posts = Post.objects.filter(author=profile_owner,published_date__lte=timezone.now()).order_by('published_date')
    
    friends = Friend.objects.friends(profile_owner)
    following = Follow.objects.following(profile_owner)
    followers = Follow.objects.followers(profile_owner)
    friend_requests = Friend.objects.unread_requests(user=profile_owner)
    return render(request, 'blog/profile.html', {'user': request.user, 'profile_owner': profile_owner, 'posts': posts, 'friends': friends, 'following':following, 'followers':followers, 'friend_requests':friend_requests})

def send_friend_request(request, pk):
    other_user = User.objects.get(id = pk)
    Friend.objects.add_friend(request.user, other_user, message = 'I would like to request your friendship.')
    return render(request, 'blog/profile.html', {'user': request.user, 'other_user': other_user, 'posts': posts})

def accept_friend_request(request, pk):
    friend_request = FriendshipRequest.objects.get_object_or_404(pk = pk)
    friend_request.accept_friend_request()
    return render(request, 'blog/profile.html', {'user': request.user})

def reject_friend_request(request, pk):
    friend_request = FriendshipRequest.objects.get_object_or_404(pk = pk)
    friend_request.reject_friend_request()
    return render(request, 'blog/profile.html', {'user': request.user})

def cancel_friend_request(request, pk):
    friend_request = FriendshipRequest.objects.get_object_or_404(pk = pk)
    friend_request.cancel_friend_request()
    return render(request, 'blog/profile.html', {'user': request.user})

def show_friends(request, pk):
    if request.method =="GET":
        return Friend.objects.friends(request.user)

def git(request, pk):
    if request.method =="GET":
        profile_owner = User.objects.get(id=pk)
        posts = Post.objects.filter(author=profile_owner,published_date__lte=timezone.now()).order_by('published_date')
        
        friends = Friend.objects.friends(profile_owner)
        following = Follow.objects.following(profile_owner)
        followers = Follow.objects.followers(profile_owner)
        friend_requests = Friend.objects.unread_requests(user=profile_owner)
        return render(request, 'blog/profile.html', {'user': request.user, 'profile_owner': profile_owner, 'posts': posts, 'friends': friends, 'following':following, 'followers':followers, 'friend_requests':friend_requests})
