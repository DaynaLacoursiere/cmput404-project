from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from .models import Post, User, SockPost, Squire, Comment
import models
from .forms import PostForm, CommentForm, UserRegForm, GitRegForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from friendship.models import Friend, Follow, FriendshipRequest
from django.template.context_processors import csrf
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.core import serializers
import uuid
import requests

def gitParse(payload):
    i = 0

    # Loop should in theory, exit even if i goes to infinity.
    # This is just a safety method until a "better" way to do this is found.
    while(i < 100):

        # This will only fail if we run out of events.
        try:
            eventType = payload.json()[i]['type']

        # Out of valid events, just leave a generic message.
        except:
            return " checkout their Github for more details!"

        # Try to find one of these events, if not move to the next.
        else:
            print(eventType)
            if (eventType == "PushEvent"):
                # This try is necessary for really dumb reasons. Update your API Github! You butts!
                try:
                    number = payload.json()[i]['payload']['size']
                except:
                    number = " a "
                repo = payload.json()[i]['repo']['name']
                return " pushed "+ str(number) + " commit(s) to "+ str(repo)+"."
            elif (eventType == "WatchEvent"):
                repo = payload.json()[i]['repo']['name']
                return " starred the repository "+str(repo)+"."
            elif (eventType == "CreateEvent"):
                repo = payload.json()[i]['repo']['name']
                return " created the repository "+str(repo)+"."
            elif (eventType == "CommitCommentEvent"):
                repo = payload.json()[i]['repo']['name']
                comment = payload.json()[i]['payload']['comment']['body']
                return ' commented "'+str(comment)+'" on a commit to '+str(repo)+"."
            elif (eventType == "ForkEvent"):
                repo = payload.json()[i]['repo']['name']
                return " forked the repository "+str(repo)+"."
            elif (eventType == "IssueCommentEvent"):
                repo = payload.json()[i]['repo']['name']
                comment = payload.json()[i]['payload']['comment']['body']
                return ' commented "'+str(comment)+'" on an issue in the repository '+str(repo)+"."
            elif (eventType == "IssuesEvent"):
                action = payload.json()[i]['payload']['action']
                title = payload.json()[i]['payload']['issue']['title']
                repo = payload.json()[i]['repo']['name']
                return " "+str(action)+' the "'+str(title)+'" issue on the repository '+str(repo)+"."
            elif (eventType == "LabelEvent"):
                action = payload.json()[i]['payload']['action']
                repo = payload.json()[i]['repo']['name']
                return " "+str(action)+' the label on the repository '+str(repo)+"."   
            else:
                i += 1

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.is_active=False
            user.save()
            return HttpResponseRedirect('/reg/confirm')
    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/user_signup.html', token)


def registration_complete(request):
    return render_to_response('registration/register_success.html')

def gitregister(request):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    if request.method == 'POST':
        form = GitRegForm(request.POST)
        if form.is_valid():
            gituser = form.cleaned_data['username']
            user_agent = {'User-agent': gituser}
            r = requests.get('https://api.github.com/users/'+gituser+'/events', headers=user_agent)

            # If the github username is valid, this will succeed.
            if (r.status_code == 200 and len(r.json()) > 0):
                #Involves another requests to /../events of that user.
                eventType = r.json()[0]['type']

                # I need to rework how we parse these since they can change drastically between users. For now we paste raw payload data.
                eventURL = r.json()[0]
                eventMessage = r.json()[0]

                # Message for team: How do I make a post out of this?
                postTitle = gituser + " has a new " + eventType + "."
                postMessage = gituser+gitParse(r)

                # Attempt
                gitPost = models.Post(author=request.user, text=postMessage, title=postTitle, published_date=timezone.now(), image='github.png')
                gitPost.save()

                return HttpResponseRedirect('/git/confirm')
            else:
                # Fails silently. Needs fix.
                form = GitRegForm()
                return render(request, 'registration/git_signup.html', {'form': form})
    else:
        form = GitRegForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/git_signup.html', token)

def git_registration_complete(request):

    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    return render_to_response('registration/git_register_success.html')

def login(request):
    if not(request.user.is_anonymous()):
        return render(request, 'registration/already_authenticated.html')
    form = PostForm()
    return render(request, 'blog/login.html', {'form': form})

def mutual_friends(list_a, list_b):
        for friend in list_a:
            if friend in list_b:
                return True
        return False


def post_list(request):

    if (request.user.is_anonymous()):
        return render(request, 'blog/splash_page.html')

    # Socknet Posts
    headers = {'User-agent': 'SquireSpace'}
    try:
        socknetjson = requests.get('http://cmput404f16t04dev.herokuapp.com/api/posts/', headers=headers, auth=('admin', 'cmput404'))
        assert(socknetjson.status_code == 200)
    except:
        print("Failed to grab SockNet API")
    else:
        for i in socknetjson.json()['posts']:
            sauthor = str(i['author']['displayName'])
            stitle = str(i['title'])
            stext = str(i['content'])
            sid = i['id']

            # If it's a new SockNet poster, make a fake user on their behalf.
            if (len(User.objects.filter(username=sauthor)) == 0):
                suser = User.objects.create_user(sauthor, 'socknet@socknet.com', str(uuid.uuid4))
                suser.save()

            sockPost = models.Post(author=User.objects.filter(username=sauthor)[0], text=stext, title=stitle, id=sid, image='sock.png', published_date=timezone.now(), source="SockNet", host="SockNet")
            if (len(Post.objects.filter(id=sid)) == 0):
                sockPost.save()

            # Now we handle comments!
            if (len(i['comments']) > 0):
                for j in i['comments']:
                    cid = j['id']
                    ctext = j['comment']
                    cauthor = j['author']['displayName']
                    # If it's a new SockNet poster, make a fake user on their behalf.
                    if (len(User.objects.filter(username=cauthor)) == 0):
                        cuser = User.objects.create_user(cauthor, 'socknet@socknet.com', str(uuid.uuid4))
                        cuser.save()
                    else:
                        cuser = User.objects.filter(username=cauthor)[0]

                    sockComm = models.Comment(post=sockPost, author=cuser, text=ctext, id=cid, created_date=timezone.now())
                    if (len(Comment.objects.filter(id=cid)) == 0):
                        sockComm.save()
        
    
    all_posts = Post.objects.filter(published_date__lte=timezone.now())
    
    #REQUEST ABOVE WORKS BUT NEED TO PARSE IT INTO OBJECTS
    friends = Friend.objects.friends(request.user)

    # Only show posts that the current user should be able to see
    posts = []
    for post in all_posts:
        if post.author == request.user:
            posts.append(post)

        elif post.privatelevel == "public":
            posts.append(post)

        elif post.privatelevel == "friends":
            if post.author in friends:
                posts.append(post)

        elif post.privatelevel == "friends_of_friends":
            author_friends = Friend.objects.friends(post.author)

            if post.author in friends:
                posts.append(post)

            elif hasMutualFriend(friends, author_friends):
                posts.append(post)

        elif post.privatelevel == "host_friends":
            if post.host == "squirespace" and post.author in friends:
                posts.append(post)

        # else: don't show post

    return render(request, 'blog/post_list.html', {'posts': posts, 'friends': friends})

def hasMutualFriend(friends1, friends2):
    for friend in friends1:
        if friend in friends2:
            return True
    return False


def post_detail(request, pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
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
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
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
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
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
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def profile(request,pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    squire = Squire.objects.get(theUUID=pk)
    profile_owner = User.objects.get(id=squire.user.id)
    posts = Post.objects.filter(author=profile_owner,published_date__lte=timezone.now()).order_by('published_date')
    friends = Friend.objects.friends(profile_owner)
    following = Follow.objects.following(profile_owner)
    followers = Follow.objects.followers(profile_owner)
    friend_requests = Friend.objects.unrejected_requests(user=profile_owner)
    return render(request, 'blog/profile.html', {'user': request.user, 'profile_owner': profile_owner, 'posts': posts, 'friends': friends, 'following':following, 'followers':followers, 'friend_requests':friend_requests})


def send_friend_request(request, pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    # NEED TO CHECK IF FRIEND IS ANONYMOUSUSER (FRIEND.IS_ANONYMOUS())

    squire = Squire.objects.get(theUUID=pk)
    profile_owner = User.objects.get(id=squire.user.id)
    Friend.objects.add_friend(request.user, profile_owner, message = 'I would like to request your friendship.')
    return profile(request, pk)

def accept_friend_request(request, pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    # NEED TO CHECK IF FRIEND IS ANONYMOUSUSER (FRIEND.IS_ANONYMOUS())
    friend_request = FriendshipRequest.objects.get(pk = pk)
    friend_request.accept_friend_request()
    return profile(request, pk)

def reject_friend_request(request, pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    # NEED TO CHECK IF FRIEND IS ANONYMOUSUSER (FRIEND.IS_ANONYMOUS())
    friend_request = FriendshipRequest.objects.get(pk = pk)
    friend_request.reject_friend_request()
    return profile(request, pk)
    
def cancel_friend_request(request, pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    # NEED TO CHECK IF FRIEND IS ANONYMOUSUSER (FRIEND.IS_ANONYMOUS())
    friend_request = FriendshipRequest.objects.get(pk = pk)
    profile_owner = friend_request.to_user.id
    friend_request.cancel()
    return profile(request, profile_owner)

def remove_friend(request, pk):
    profile_owner = User.objects.get(id = pk)
    Friend.objects.remove_friend(request.user, profile_owner)
    return profile(request, pk)

def show_friends(request, pk):
    if (request.user.is_anonymous()):
        return render(request, 'blog/401.html')
    if request.method =="GET":
        return Friend.objects.friends(request.user)

def page_not_found(request):
    return render(request, 'blog/404.html')
