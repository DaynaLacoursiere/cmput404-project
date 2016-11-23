from django.contrib.auth.models import User
from blog.models import Post, Comment
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    displayName = serializers.SerializerMethodField('getDisplayName')
    host = serializers.SerializerMethodField('getHostName')
    url = serializers.SerializerMethodField('getURL')
    id = serializers.SerializerMethodField('getID')
    github = serializers.SerializerMethodField('getGithub')
    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'github')

    def getDisplayName(self, obj):
        return obj.username

    def getHostName(self, obj):
        return "squirespace"

    def getURL(self,obj):
        return "http://aedan.pythonanywhere.com"

    def getID(self,obj):
        return obj.squire.theUUID
        # return obj.id #change to uuid

    def getGithub(sefl,obj):
        return ""


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comment = serializers.CharField(source='text')
    published = serializers.CharField(source='text')
    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'id')

class PostSerializer(serializers.ModelSerializer):
    # rename text field from post model to content in JSON
    content = serializers.CharField(source='text')
    origin = serializers.CharField(source='host')
    author = UserSerializer()
    comments = CommentSerializer(required=False, many=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'source','origin',  'description', 'contentType', 'author', 'content', 'comments')

class PostSerializerNoComments(serializers.ModelSerializer):
    # rename text field from post model to content in JSON
    content = serializers.CharField(source='text')
    origin = serializers.CharField(source='host')
    class Meta:
        model = Post
        fields = ('id', 'title', 'source','origin',  'description', 'contentType', 'author', 'content')
