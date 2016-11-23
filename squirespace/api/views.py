from django.contrib.auth.models import User
from django.http import Http404
from blog.models import Post, Comment
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import render, get_object_or_404 
from rest_framework.pagination import *
from friendship.models import Friend, Follow, FriendshipRequest
import json

'''
this snippet of code from http://www.django-rest-framework.org/api-guide/authentication/#BasicAuthentication,
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
and
    (in get functions)
     content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
will be used in almost all APIViews
'''
class UserList(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def post(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(user.data)

    def put(self, request, pk, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class UserPosts(APIView):
    
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        author = self.get_object(pk)
        posts = Post.objects.all()
        userposts = []
        for post in posts:
            if post.author.id is author.id:
                userposts.append(post)

        serializer = PostSerializer(userposts, many=True)
        return Response(serializer.data)


class UserViewablePosts(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def mutual_friends(self, list_a, list_b):
        print list_a
        print list_b
        for friend in list_a:
            print "Friend from list A"
            print friend
            if friend in list_b:
                print "Friend is in list B too!!!"
                return True
        return False

    def get(self, request, format=None):
        user = request.user
        posts = Post.objects.all()
        friends = Friend.objects.friends(user);
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        
        userViewablePosts = []

        for post in posts:
            author = post.author
            authorfriends = Friend.objects.friends(author);
            # They're the author
            if post.author.id is user.id:
                userViewablePosts.append(post)
            elif post.privatelevel == "public":
                userViewablePosts.append(post)
            elif post.privatelevel == "friends":
                # Check if user and author are friends
                if author in friends:
                    userViewablePosts.append(post)
            elif post.privatelevel == "friends_of_friends":
                # Check if author and user have a mutual friend
                if self.mutual_friends(authorfriends, friends):
                    userViewablePosts.append(post)
            elif post.privatelevel == "host_friends":
                # Check if user and author are from the same host
                # Then check that they're friends

                ## hostnames are not implemented yet
                # if user.hostname == author.hostname:
                #     if author in friends:
                #         userViewablePosts.append(post)
                print "Check host friends"

            # else: Don't show the post

        serializer = PostSerializer(userViewablePosts, many=True)
        return Response(serializer.data)


class PostList(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        posts = Post.objects.all()
        pagination_class = PostPaginate() # pagination not working for performed automatically for generic views
        #http://www.django-rest-framework.org/api-guide/pagination/
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)



class VisiblePostList(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        friends = Friend.objects.friends(request.user)
        posts = Post.objects.all()
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)



class PostDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        post = self.get_object(pk)
        post = PostSerializerNoComments(post)
        return Response(post.data)



class Comments(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.all().filter(post = post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)



class PostDetailComments(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        post = self.get_object(pk)
        post = PostSerializer(post)
        return Response(post.data)

    def post(self, request, pk):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        post = self.get_object(pk)
        #serializer = CommentSerializer

        author = request.user
        Comment.objects.create(author=author,post=post, text = comment)
        post = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostPaginate(PageNumberPagination):
	page_size = 2
	page_size_query_param = 'page_size'
	max_page_size = 2
    

class CommentPaginate():
	page_size = 5
	page_size_query_param = 'page_size'
	max_page_size = 100

class UsersFriends(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        friends = Friend.objects.friends(user);
        friendsIds = []
        for friend in friends:
            friendsIds.append(friend.squire.theUUID)

        content = {
            'query':'friends',
            'authors':friendsIds,
        }

        return Response(content)

class AreTheseTwoUsersFriends(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404



    def get(self, request, pk1, pk2, format=None):

        user1 = self.get_object(pk1)
        user2 = self.get_object(pk2)
        isFriends = False
        if(Friend.objects.are_friends(user1, user2) and Friend.objects.are_friends(user2, user1)):
            isFriends = True
        
        content = {
            'query':'friends',
            'authors':[ user1.squire.theUUID, user2.squire.theUUID],
            'friends':isFriends,
        }

        return Response(content)









