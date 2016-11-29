from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import markdownfunctions
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
	host = models.TextField(default="squirespace")

	source = models.TextField(default="squirespace")

	markdown=models.BooleanField(default=False)
	source = models.TextField(default="http://aedan.pythonanywhere.com/")
	id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

	description = "this is a post"
	contentType = "text/plain"
	PRIVATE_LEVEL_CHOICES = (
			('PUBLIC','Public'),
			('FRIENDS','Private: Friends Only'),
			('FOAF','Private: Friends of Friends'),
			('SERVERONLY','Private: Friends on my Host Only'),
			('PRIVATE','Private: Me Only')
		)
		
	privatelevel = models.CharField(verbose_name="Privacy level of post:", default='PUBLIC', max_length=200, choices=PRIVATE_LEVEL_CHOICES)


	def publish(self):
		self.published_date = timezone.now()
		self.save()
	def get_markdown(self):
		#add a check if users want to markdown stuff
		return markdownfunctions.markdown_stuff(self.text, self.markdown)

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
    markdown=models.BooleanField(default=False)
    theUUID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    contentType = "text/plain"
    def __str__(self):
        return self.text
    def get_markdown(self):
		#add a check if users want to markdown stuff
		return markdownfunctions.markdown_stuff(self.text, self.markdown)


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
	theUUID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
	admin_approve=models.BooleanField(default=False)
	hostname=models.TextField(default="SquireSpace", editable=False)

	def __str__(self):
		return self.user.username+" - UUID: "+str(self.theUUID)

#This creates a Squire everytime a user is made.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Squire.objects.create(user=instance)











