from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# Create your models here.

class Post(models.Model):
	#author = models.ForeignKey('auth.User')
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
    )
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank = True, null = True)
	image = models.ImageField(upload_to='',default='default.png', blank=True)
	host = "squirespace"

	id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

	description = "this is a post"
	contentType = "text/plain"
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

#This model has been migrated but isn't used for shit.
class SockPost(models.Model):
	author = models.TextField()
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank = True, null = True)
	image = models.ImageField(upload_to='',default='default.png', blank=True)
	host = "socknet"
	id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
	description = "this is a post"
	contentType = "text/plain"


	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    theUUID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    contentType = "text/plain"
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

# Extend default user. Has a UUID. NOT ACTUALLY REPLACING OUR USER MODEL.
class Squire(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	theUUID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	admin_approve=models.BooleanField(default=False)
	hostname=models.TextField(default="SquireSpace", editable=False)

	def __str__(self):
		return self.user.username+" - UUID: "+str(self.theUUID)

#This creates a Squire everytime a user is made.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Squire.objects.create(user=instance)











