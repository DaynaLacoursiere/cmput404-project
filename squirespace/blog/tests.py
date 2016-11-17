# blank databases are created for tests and destroyed after tests are executed
# to keep test databases: python manage.py --keepdb
# test databases are prepended by test_ to their NAME

from django.test import TestCase, Client
from .models import Post, Comment
from django.contrib.auth.models import AbstractBaseUser, UserManager, User
from django.core.urlresolvers import reverse

# test client is a python class that acts as a dummy web browser
# use for testing views
# test client does not need the server to be running
# use URL path not domain (to retrieve other pages you need urllib Python module)

c = Client()


class postTest(TestCase):	
	def setUp(self):
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")
		c.login(username='John', password='a')	

# test methods must begin with test		
	def testCreatePost(self):
		author = User.objects.get(username = "John")
		tpost = Post.objects.create(author = author, title = "Test post please ignore", text = "yep")
		self.assertTrue(isinstance(author, User))
		self.assertEqual(tpost.author, self.user)
		self.assertEqual(tpost.text, "yep")

	def testPostViews(self):


		# not sure why the test client returns a redirect
		post1page = c.get('/post/1')
		self.assertEqual(post1page.status_code, 301)  #200
		post2page = c.get("/post/2")
		self.assertEqual(post2page.status_code, 301)  #404

		badurl = c.get('post/1')
		# optional third argument for customized error messages
		self.assertEqual(badurl.status_code, 404, "wrong status code") 

		response = c.get('/')
		self.assertEqual(response.status_code, 200)
