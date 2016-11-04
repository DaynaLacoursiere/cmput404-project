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
	title=forms.ChoiceField(choices=TITLES, required=True)
	nation=forms.ChoiceField(choices=NATIONS, required=True)

	class Meta:
		model=User
		fields=('title', 'first_name', 'nation', 'email', 'password',)
		widgets={
			'first_name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'john@example.com'}),
			'password': forms.PasswordInput(),
			}

