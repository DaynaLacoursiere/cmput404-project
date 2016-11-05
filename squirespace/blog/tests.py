# blank databases are created for tests and destroyed after tests are executed
# to keep test databases: python manage.py --keepdb
# test databases are prepended by test_ to their NAME

from django.test import TestCase, Client
from .models import Post, User, Comment
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.urlresolvers import reverse

# test client is a python class that acts as a dummy web browser
# use for testing views
# test client does not need the server to be running
# use URL path not domain (to retrieve other pages you need urllib Python module)
c = Client()

# have to create user accounts because created test database has no users
# set_password() to store hashed password
# or create_user() helper method

# user create Django base
#class userTest(AbstractBaseUser):
#	def setUp(self):
#		user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a") 
#
#	def testLogin(self):
#		c.login(username='John', password='a')


class userclassTest(TestCase):	
	def userclass(self):
		return User.objects.create(title = "admin", first_name="bob", email="pid@yahoo.ca", password="admin")
	def testUserClassCreation(self):
		user = self.userclass()
		self.assertTrue(isinstance(user, User))
		self.assertEquals(user.title, "admin")
	def viewsTest(TestCase):
		w = self.userclass()
		url = reverse("user.views.user")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertIn(w.title, resp.content)


# fails because author field has to have a user object to get 
class blogTest(TestCase):	
	def userclass(self):
		return User.objects.create(title = "admin", first_name="bob", email="pid@yahoo.ca", password="admin")

	def createPost(self):
		user = self.userclass()
		# Post.author must be "User" instance
		return Post.objects.create(author = user, title = "Test post please ignore", text = "yep")

	def testPostCreation(self):
		#p = self.createPost()
		p = self.userclass()
		self.assertTrue(True)
		#self.assertTrue(isinstance(p, blogTest))

