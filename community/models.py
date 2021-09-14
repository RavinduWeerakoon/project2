from django.db import models

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import re
# Create your models here.



from django.contrib.auth.models import AbstractUser,UserManager

class CustomUser(AbstractUser):
	objects = UserManager()

@receiver(post_save, sender=CustomUser)
def user_callback(sender, instance,created, *args, **kwargs):
	if created:
		t_user = TubeUser.objects.create(user=instance)    


class TubeUser(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	tube_url = models.URLField(blank=True, null=True)
	viewed_users = models.ManyToManyField('self', blank=True)
	subscribed_users = models.ManyToManyField('self', blank=True)

	def __str__(self):
		return self.user.username

    

class Video(models.Model):
	user = models.ForeignKey(TubeUser, on_delete=models.CASCADE)
	embed_script = models.TextField(null=True, blank=True)
	url = models.URLField()
	time = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.url

@receiver(pre_save, sender=Video)
def my_callback(sender, instance, *args, **kwargs):
    url = instance.url
    embed = url.replace('https://youtu.be', 'https://www.youtube.com/embed')
    
    instance.embed_script = embed






class Contact(models.Model):
	email = models.EmailField()
	message = models.TextField()

	def __str__(self):
		return self.email

