from django.test import TestCase
from .models import TubeUser, Video
from django.contrib.auth.models import User 

# Create your tests here.


class GetVideoTest(TestCase):

	def create_models(self):
		u1 = User.objects.create(username="abc", password="abc")
		u2 = User.objects.create(username="hiran", password="hiran")
		u3 = User.objects.create(username="bandara", password="bandara")
		t1 = TubeUser.objects.create(user=u1,tube_url="https://bls.com")
		t2 = TubeUser.objects.create(user=u2, tube_url="https://abn.com")
		t3 = TubeUser.objects.create(user=u3, tube_url="https://fontawesome.com")
		# t1.viewed_users.add(t2)
		v1 = Video.objects.create(user=t2, embed_script="basn asdbas asd", url="https://blahblah.com")
		v2 = Video.objects.create(user=t3, embed_script="Ravindu Weerakoon", url="https://yourube.be")
		return (u1,u2,t1,t2,t3,v1,v2)

	def test_get_video(self):
		from .views import get_video 
		u1,u2,t1,t2,t3,v1,v2 = self.create_models()
		t1.subscribed_users.add(t3)
		print(get_video(u1))
		# print(t2.viewed_users.all())		




