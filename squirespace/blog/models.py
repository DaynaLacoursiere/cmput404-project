from __future__ import unicode_literals
from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank = True, null = True)
	image = models.ImageField(upload_to='',default='default.png', blank=True)
	host = "squirespace"
	#unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

	PRIVATE_LEVEL_CHOICES = (
			('public','Public'),
			('friends','Private: Friends Only'),
			('friends_of_friends','Private: Friends of Friends'),
			('host_friends','Private: Friends on my Host Only'),
			('only_me','Private: Me Only')
		)
		
	privatelevel = models.CharField(verbose_name="Privacy level of post:", default=PRIVATE_LEVEL_CHOICES[0], max_length=200, choices=PRIVATE_LEVEL_CHOICES)


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
    #unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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

class Squire(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	#title=models.CharField(max_length=3, choices=TITLES)
	#first_name= models.CharField(max_length=200)
	#nation=models.CharField(max_length=3, choices=NATIONS)
	#email=models.EmailField()
	#password=models.CharField(max_length=200)
	admin_approve=models.BooleanField()














