from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic import FormView
from .models import Post, User
from .forms import PostForm, CommentForm, UserRegForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf


class UserRegPage(FormView):
    template_name='blog/user_signup.html'
    success_url='/reg/confirm'
    form_class = UserRegForm
    

def user_registration(request):
    if request.method == "POST":
        form=UserRegForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            first_name = form.cleaned_data['first_name']
            nation = form.cleaned_data['nation']
            email=form.cleaned_data['email']
            password= form.cleaned_data['password']
            user=User.objects.create_user(title,first_name,nation,email,password)
            form.save()
            return HttpResponseRedirect('registration/register_success')
    args = {}
    args.update(csrf(request))
    args['form'] = UserRegForm()
    return render_to_response('user_signup.html',args)

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