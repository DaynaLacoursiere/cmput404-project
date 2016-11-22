from django.contrib.auth.models import User
from django.http import Http404
from blog.models import Post, Comment
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404 
from rest_framework.pagination import *

class UserList(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
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
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostList(APIView):

    def get(self, request, format=None):
        posts = Post.objects.all()
        pagination_class = PostPaginate() # pagination not working for performed automatically for generic views
        #http://www.django-rest-framework.org/api-guide/pagination/

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

class VisiblePostList(APIView):

    def get(self, request, format=None):
        friends = Friend.objects.friends(request.user)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)




class PostDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        post = PostSerializerNoComments(post)
        return Response(post.data)

class Comments(APIView):


    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.all().filter(post = post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class PostDetailComments(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        post = PostSerializer(post)
        return Response(post.data)

    def post(self, request, pk):
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
