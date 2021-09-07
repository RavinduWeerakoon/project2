from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



from django.contrib.auth.models import AbstractUser,UserManager

class CustomUser(AbstractUser):
	objects = UserManager()
    


class TubeUser(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	tube_url = models.URLField()
	viewed_users = models.ManyToManyField('self', blank=True)
	subscribed_users = models.ManyToManyField('self', blank=True)

	def __str__(self):
		return self.tube_url

    

class Video(models.Model):
	user = models.ForeignKey(TubeUser, on_delete=models.CASCADE)
	embed_script = models.TextField()
	url = models.URLField()
	time = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.url

class Contact(models.Model):
	email = models.EmailField()
	message = models.TextField()

	def __str__(self):
		return self.email

