from django.test import TestCase, Client
from django.contrib.auth.models import AbstractBaseUser, UserManager, User

# Create your tests here.
c = Client()

class UserApiTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = "John", email = "john@mailinator.com", password="a")
		c.login(username='John', password='a')	
	def testUserApiGet(self):
		req = c.get('/api/users/1')
		self.assertEqual(req.status_code, 200)
		req = c.get('/api/users/2')
		self.assertEqual(req.status_code, 404)

	def testUserApiPost(self):
		req = c.post('/api/users/', {"username":"xxz", "email":"xx@x.ca"})
		self.assertEqual(req.status_code, 201) #201 is Created