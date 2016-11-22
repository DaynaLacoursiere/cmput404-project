from django.contrib.auth.models import User
from blog.models import Post, Comment
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('theUUID', 'id', 'author', 'title', 'text', 'created_date', 'published_date', 'image', 'host')


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('theUUID', 'post', 'author', 'text', 'created_date')


