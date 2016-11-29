from django import forms

from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'privatelevel', 'markdown')
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', 'markdown')


class UserRegForm(forms.ModelForm):

	def __init__(self):
		self.fields['admin_approve'](initial = False)

	class Meta:
		model=User
		fields=('username', 'email', 'password')


class GitRegForm(forms.Form):

	username = forms.CharField(label='Github Username')