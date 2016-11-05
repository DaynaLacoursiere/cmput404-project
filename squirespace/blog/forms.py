from django import forms

from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
        

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

	class Meta:
		model=User
		fields=('username', 'email', 'password')
		

