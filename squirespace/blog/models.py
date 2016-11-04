from __future__ import unicode_literals
from django import forms
from django.db import models
from django.utils import timezone
# Create your models here.

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(
		default=timezone.now)
	published_date = models.DateTimeField(
		blank = True, null = True)
	image = models.ImageField(upload_to='',default='default.png', blank=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text



TITLES=(
	('SQR', 'Squire'),
	('SIR', 'Sir'),
	('DME', 'Dame'),
	)
NATIONS = (
	('GDR','Gondor'),
	('RHN', 'Rohan'),
	('MDR', 'Mordor')
	)
class User(models.Model):
	title=models.CharField(max_length=3, choices=TITLES)
	first_name= models.CharField(max_length=200)
	nation=models.CharField(max_length=3, choices=NATIONS)
	email=models.EmailField()
	password=models.CharField(max_length=200)

class Friendship(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey('auth.User', related_name="friendship_sender")
    friend = models.ForeignKey('auth.User', related_name="friendship_receiver")


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey('auth.User', related_name="invitations_from")
    to_user = models.ForeignKey('auth.User', related_name="invitations_to")
    created = models.DateTimeField(auto_now_add=True,editable=False)
    accepted = models.BooleanField(default=False)

    def accept(self):
        self.accepted = True
        self.delete()

    def decline(self):
        self.delete()

    def cancel(self):
        self.delete()











