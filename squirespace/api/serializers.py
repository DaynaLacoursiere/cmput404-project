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
    published = serializers.DateTimeField(source='created_date')
    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'id')

class PostSerializer(serializers.ModelSerializer):
    # rename text field from post model to content in JSON
    content = serializers.CharField(source='text')
    origin = serializers.SerializerMethodField('getURL')
    author = UserSerializer()
    published = serializers.DateTimeField(source='published_date')
    comments = CommentSerializer(required=False, many=True)
    visibility = serializers.CharField(source='privatelevel')
    categories = serializers.SerializerMethodField('getcategories')
    count = serializers.SerializerMethodField('getplaceholder')
    size = serializers.SerializerMethodField('getplaceholder') 
    next = serializers.SerializerMethodField('getplaceholder')
    source = serializers.SerializerMethodField('getURL')
    
    class Meta:
        model = Post
        fields = ('title', 'source','origin',  'description', 'contentType', 'content', 'author','categories', 'count','size', 'next', 'comments', 'published', 'id','visibility')

    def getcategories(self,obj):
        return "none"
    
    def getplaceholder(self,obj):
        return "0"

    def getURL(self,obj):
        return "http://aedan.pythonanywhere.com/post/"+str(obj.id)



class PostSerializerNoComments(serializers.ModelSerializer):
    content = serializers.CharField(source='text')
    origin = serializers.SerializerMethodField('getURL')
    author = UserSerializer()
    published = serializers.DateTimeField(source='published_date')
    visibility = serializers.CharField(source='privatelevel')
    categories = serializers.SerializerMethodField('getcategories')
    count = serializers.SerializerMethodField('getplaceholder')
    size = serializers.SerializerMethodField('getplaceholder')
    next = serializers.SerializerMethodField('getplaceholder')
    source = serializers.SerializerMethodField('getURL')
    class Meta:
        model = Post
        fields = ('title', 'source','origin',  'description', 'contentType', 'content', 'author','categories', 'count','size', 'next', 'published', 'id','visibility')

    def getcategories(self,obj):
        return "none"
    
    def getplaceholder(self,obj):
        return "0"

    def getURL(self,obj):
        return "http://aedan.pythonanywhere.com/post/"+str(obj.id)































        
