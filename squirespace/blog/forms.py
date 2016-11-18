from django import forms

from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'privatelevel', 'otherauthor')
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)



TITLES=(
	('NLL', "----"),
	('SQR', 'Squire'),
	('SIR', 'Sir'),
	('DME', 'Dame'),
	)
NATIONS = (
	('NLL', "----"),
	('GDR','Gondor'),
	('RHN', 'Rohan'),
	('MDR', 'Mordor')
	)

class UserRegForm(forms.ModelForm):

	def __init__(self):
		self.fields['admin_approve'](initial = False)

	class Meta:
		model=User
		fields=('username', 'email', 'password')

class gitForm(forms.ModelForm):

	def __init__(self):
		self.fields['user_approve'](initial = False)

	class Meta:
		model=User
		fields=('username',)